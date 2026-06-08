from app.services.ai_service import review_submission
from app.services.ai_service import extract_progress
from app.services.ai_service import ask_gemini
from app.services.ai_service import extract_assignment_details
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.models.teacher import Teacher
from app.models.student import Student
from app.models.assignment import Assignment
from app.models.assignment_submission import AssignmentSubmission
from app.db import get_db

BOT_TOKEN = "8664074250:AAGHI1C6S1cLxX5xH4nc7kiOCWo6-DqznHE"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Classroom Companion Bot is running 🚀"
    )


async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db = get_db()

    telegram_id = str(update.effective_user.id)
    username = update.effective_user.username
    name = update.effective_user.first_name

    existing_teacher = (
        db.query(Teacher)
        .filter(Teacher.telegram_id == telegram_id)
        .first()
    )

    if existing_teacher:
        await update.message.reply_text(
            "You are already registered as a teacher."
        )
        return

    new_teacher = Teacher(
        telegram_id=telegram_id,
        username=username,
        name=name
    )

    db.add(new_teacher)
    db.commit()

    await update.message.reply_text(
        "Registered as Teacher successfully ✅"
    )
async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db = get_db()

    telegram_id = str(update.effective_user.id)
    username = update.effective_user.username
    name = update.effective_user.first_name

    existing_student = (
        db.query(Student)
        .filter(Student.telegram_id == telegram_id)
        .first()
    )

    if existing_student:
        await update.message.reply_text(
            "You are already registered as a student."
        )
        return

    new_student = Student(
        telegram_id=telegram_id,
        username=username,
        name=name
    )

    db.add(new_student)
    db.commit()

    await update.message.reply_text(
        "Registered as Student successfully ✅"
    )
async def create_assignment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage: /create_assignment <title> <deadline>"
        )

        return

    title = " ".join(context.args[:-1])

    deadline = context.args[-1]

    assignment = Assignment(
        title=title,
        description=title,
        deadline=deadline,
        status="Pending"
    )

    db.add(assignment)
    db.commit()

    await update.message.reply_text(
        f"Assignment '{title}' created successfully ✅\n"
        f"Deadline: {deadline}"
    )
async def assign(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage: /assign <student_id> <assignment_id>"
        )

        return

    student_id = int(context.args[0])
    assignment_id = int(context.args[1])

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    assignment = (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )

    if not student:

        await update.message.reply_text(
            "Student not found."
        )

        return

    if not assignment:

        await update.message.reply_text(
            "Assignment not found."
        )

        return

    submission = AssignmentSubmission(
        student_id=student.id,
        assignment_id=assignment.id,
        status="Pending"
    )

    db.add(submission)
    db.commit()

    await update.message.reply_text(
        "Assignment assigned successfully ✅"
    )
async def view_assignments(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    telegram_id = str(update.effective_user.id)

    student = (
        db.query(Student)
        .filter(
            Student.telegram_id == telegram_id
        )
        .first()
    )

    if not student:

        await update.message.reply_text(
            "Student not registered."
        )

        return

    submissions = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.student_id == student.id
        )
        .all()
    )

    if not submissions:

        await update.message.reply_text(
            "No assignments assigned."
        )

        return

    message = ""

    for submission in submissions:

        assignment = (
            db.query(Assignment)
            .filter(
                Assignment.id ==
                submission.assignment_id
            )
            .first()
        )

        message += (
            f"{assignment.title}"
            f" - {submission.status}\n"
        )

    await update.message.reply_text(
        message
    )
async def submit(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    telegram_id = str(
        update.effective_user.id
    )

    student = (
        db.query(Student)
        .filter(
            Student.telegram_id == telegram_id
        )
        .first()
    )

    if not student:

        await update.message.reply_text(
            "Student not registered."
        )

        return

    submission = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.student_id
            == student.id
        )
        .first()
    )

    if not submission:

        await update.message.reply_text(
            "No assigned assignment found."
        )

        return

    submission.status = "Submitted"

    db.commit()

    await update.message.reply_text(
        "Assignment submitted successfully ✅"
    )
async def review(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db = get_db()

    submission = db.query(AssignmentSubmission).first()

    if not submission:
        await update.message.reply_text(
            "No submission found."
        )
        return

    submission.status = "Reviewed"

    db.commit()

    await update.message.reply_text(
        "Assignment reviewed successfully ✅"
    )    
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db = get_db()

    submission = db.query(
        AssignmentSubmission
    ).first()

    if not submission:
        await update.message.reply_text(
            "No submission found."
        )
        return

    submission.feedback = (
        "Good work. Improve conclusion."
    )

    submission.status = "Reviewed"

    db.commit()

    await update.message.reply_text(
        "Feedback added successfully ✅"
    )  
async def view_feedback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    submission = db.query(
        AssignmentSubmission
    ).first()

    if not submission:
        await update.message.reply_text(
            "No feedback found."
        )
        return

    await update.message.reply_text(
        f"Feedback: {submission.feedback}"
    )  
async def view_submissions(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    submissions = (
        db.query(AssignmentSubmission)
        .all()
    )

    if not submissions:

        await update.message.reply_text(
            "No submissions found."
        )

        return

    message = ""

    for submission in submissions:

        student = (
            db.query(Student)
            .filter(
                Student.id ==
                submission.student_id
            )
            .first()
        )

        assignment = (
            db.query(Assignment)
            .filter(
                Assignment.id ==
                submission.assignment_id
            )
            .first()
        )

        message += (
            f"Student: {student.name}\n"
            f"Assignment: {assignment.title}\n"
            f"Status: {submission.status}\n"
            f"Submission:\n"
            f"{submission.submission_text}\n\n"
        )

    await update.message.reply_text(
        message
    )   
async def view_students(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    students = db.query(Student).all()

    if not students:
        await update.message.reply_text(
            "No students registered."
        )
        return

    message = "Registered Students:\n\n"

    for student in students:
        message += (
            f"ID: {student.id}\n"
            f"Name: {student.name}\n\n"
        )

    await update.message.reply_text(message) 
async def remind(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Reminder sent to students 🔔"
    )  
async def ask(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.args:

        await update.message.reply_text(
            "Usage: /ask <question>"
        )

        return

    prompt = " ".join(context.args)

    response = ask_gemini(prompt)

    await update.message.reply_text(
        response
    )
async def ai_assign(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    text = " ".join(context.args)

    result = extract_assignment_details(text)

    lines = result.strip().split("\n")

    student_name = (
        lines[0]
        .replace("Student:", "")
        .strip()
    )

    assignment_title = (
        lines[1]
        .replace("Assignment:", "")
        .strip()
    )

    deadline = (
        lines[2]
        .replace("Deadline:", "")
        .strip()
    )

    student = (
        db.query(Student)
        .filter(
            Student.name.ilike(f"%{student_name}%")
        )
        .first()
    )

    if not student:

        await update.message.reply_text(
            f"Student '{student_name}' not found."
        )

        return

    assignment = Assignment(
        title=assignment_title,
        description=assignment_title,
        deadline=deadline,
        status="Pending"
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    submission = AssignmentSubmission(
        student_id=student.id,
        assignment_id=assignment.id,
        status="Pending"
    )

    db.add(submission)
    db.commit()

    await update.message.reply_text(
        f"✅ Assignment created and assigned\n\n"
        f"Student: {student_name}\n"
        f"Assignment: {assignment_title}\n"
        f"Deadline: {deadline}"
    )
async def progress(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    text = " ".join(context.args)

    result = extract_progress(text)

    telegram_id = str(
        update.effective_user.id
    )

    student = (
        db.query(Student)
        .filter(
            Student.telegram_id == telegram_id
        )
        .first()
    )

    if not student:

        await update.message.reply_text(
            "Student not registered."
        )

        return

    submission = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.student_id
            == student.id
        )
        .first()
    )

    if not submission:

        await update.message.reply_text(
            "No assignment found."
        )

        return

    if "Completed" in result:

        submission.status = "Completed"

    elif "In Progress" in result:

        submission.status = "In Progress"

    db.commit()

    await update.message.reply_text(
        f"{result}\n\n"
        f"Database updated ✅"
    )
async def submit_content(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    telegram_id = str(
        update.effective_user.id
    )

    student = (
        db.query(Student)
        .filter(
            Student.telegram_id == telegram_id
        )
        .first()
    )

    if not student:

        await update.message.reply_text(
            "Student not registered."
        )

        return

    submission = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.student_id
            == student.id
        )
        .first()
    )

    if not submission:

        await update.message.reply_text(
            "No assignment found."
        )

        return

    text = " ".join(context.args)

    if not text:

        await update.message.reply_text(
            "Usage: /submit_content <your assignment text>"
        )

        return

    submission.submission_text = text

    submission.status = "Submitted"

    db.commit()

    await update.message.reply_text(
        "Assignment content submitted successfully ✅"
    )
async def ai_review(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    db = get_db()

    submissions = (
        db.query(
            AssignmentSubmission
        ).all()
    )

    if not submissions:

        await update.message.reply_text(
            "No submissions found."
        )

        return

    submission = submissions[0]

    if not submission.submission_text:

        await update.message.reply_text(
            "Student has not submitted content."
        )

        return

    result = review_submission(
        submission.submission_text
    )

    await update.message.reply_text(
        result
    )

    
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("teacher", teacher))
app.add_handler(CommandHandler("student", student))
app.add_handler(CommandHandler("create_assignment", create_assignment))
app.add_handler(CommandHandler("assign", assign))
app.add_handler(CommandHandler("view_assignments",view_assignments))
app.add_handler(CommandHandler("submit", submit))
app.add_handler(CommandHandler("review", review))
app.add_handler(CommandHandler("feedback",feedback))
app.add_handler(CommandHandler("view_feedback",view_feedback))
app.add_handler(CommandHandler("view_submissions",view_submissions))
app.add_handler(CommandHandler("view_students",view_students))
app.add_handler(CommandHandler("remind",remind))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("ai_assign",ai_assign))
app.add_handler(CommandHandler("progress",progress))
app.add_handler(CommandHandler("submit_content",submit_content))
app.add_handler(CommandHandler("ai_review",ai_review))


print("Bot started...")

app.run_polling()