from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.db import get_db
from app.models.student import Student
from fastapi import FastAPI

from app.database import engine, Base

from app.models.teacher import Teacher
from app.models.student import Student
from app.models.assignment import Assignment
from app.models.assignment_submission import AssignmentSubmission
from app.models.attendance import Attendance
from app.models.quiz import Quiz

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Classroom Companion Running"}
templates = Jinja2Templates(
    directory="templates"
)
@app.get("/teacher")
def teacher_dashboard(request: Request):

    db = get_db()

    submissions = db.query(
        AssignmentSubmission
    ).all()

    data = []

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

        data.append({
    "student": student.name,
    "assignment": assignment.title,
    "deadline": assignment.deadline,
    "submission_text": submission.submission_text,
    "status": submission.status,
    "feedback": submission.feedback
})

    total_students = db.query(Student).count()

    total_assignments = db.query(
        Assignment
    ).count()

    pending_count = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.status == "Pending"
        )
        .count()
    )

    reviewed_count = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.status == "Reviewed"
        )
        .count()
    )

    return templates.TemplateResponse(
        request=request,
        name="teacher.html",
        context={
            "data": data,
            "total_students": total_students,
            "total_assignments": total_assignments,
            "pending_count": pending_count,
            "reviewed_count": reviewed_count
        }
    )

@app.get("/student/{student_id}")
def student_dashboard(
    request: Request,
    student_id: int
):

    db = get_db()
    student = (
    db.query(Student)
    .filter(Student.id == student_id)
    .first()
)

    submissions = (
    db.query(AssignmentSubmission)
    .filter(
        AssignmentSubmission.student_id == student_id
    )
    .all()
)

    data = []

    for submission in submissions:

        assignment = (
            db.query(Assignment)
            .filter(
                Assignment.id ==
                submission.assignment_id
            )
            .first()
        )

        student = (
            db.query(Student)
            .filter(
                Student.id ==
                submission.student_id
            )
            .first()
        )

        data.append({
            "student": student.name,
            "assignment": assignment.title,
            "deadline": assignment.deadline,
            "status": submission.status,
            "feedback": submission.feedback
        })

    print("Total submissions:", len(submissions))
    print(data)

    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={
    "data": data
}
    )