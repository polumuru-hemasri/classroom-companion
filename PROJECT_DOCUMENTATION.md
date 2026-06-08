# Classroom Companion - Project Documentation

## 1. Introduction

Classroom Companion is an AI-powered classroom management system designed to simplify communication and task management between teachers and students.

The system combines a Telegram Bot, FastAPI backend, SQLite database, and Google Gemini AI to automate classroom workflows such as assignment management, feedback generation, progress tracking, and student engagement.

The project demonstrates how conversational AI can be integrated into educational environments to improve productivity and learning outcomes.

---

## 2. Problem Statement

Traditional classroom management often requires teachers to manually manage assignments, track submissions, provide feedback, and monitor student progress.

This process can become time-consuming and difficult to scale.

The goal of this project is to create an intelligent assistant that helps automate these tasks while providing a simple interface for both teachers and students.

---

## 3. Objectives

The primary objectives of the project are:

* Enable teachers to create and assign assignments.
* Allow students to view and submit assignments.
* Store all classroom data persistently.
* Provide AI-powered assignment creation and review.
* Track student progress using natural language updates.
* Offer teacher and student dashboards for monitoring activities.
* Demonstrate agent-based workflow automation using Large Language Models.

---

## 4. System Architecture

The system consists of four main layers:

### Telegram Bot Layer

The Telegram Bot serves as the primary interaction interface.

Responsibilities:

* Teacher registration
* Student registration
* Assignment management
* Submission management
* Feedback communication
* AI command execution

### FastAPI Backend Layer

The backend processes requests received from the Telegram Bot and dashboards.

Responsibilities:

* API routing
* Business logic execution
* Database interaction
* Dashboard rendering

### AI Layer

Google Gemini AI is used for natural language understanding and content generation.

Responsibilities:

* Assignment parsing
* Progress interpretation
* Question answering
* Assignment review

### Database Layer

SQLite is used for persistent storage.

Responsibilities:

* Student records
* Teacher records
* Assignment records
* Submission records
* Feedback storage

---

## 5. Technologies Used

### Backend

* Python
* FastAPI
* SQLAlchemy

### Database

* SQLite

### Artificial Intelligence

* Google Gemini API

### Bot Framework

* Python Telegram Bot

### Frontend

* HTML
* CSS
* Jinja2 Templates

---

## 6. Key Features

### Teacher Features

* Teacher registration
* Create assignments
* Assign work to students
* Review submissions
* Provide feedback
* Send reminders
* Monitor student progress

### Student Features

* Student registration
* View assignments
* Submit assignment content
* Receive feedback
* Track assignment status
* Submit progress updates

### AI Features

* Natural language assignment creation
* AI-powered assignment review
* AI question answering
* Progress interpretation

---

## 7. Database Design

### Students Table

Stores student information.

Fields:

* id
* telegram_id
* username
* name

### Teachers Table

Stores teacher information.

Fields:

* id
* telegram_id
* username
* name

### Assignments Table

Stores assignment details.

Fields:

* id
* title
* description
* deadline
* status

### Assignment Submissions Table

Stores assignment submissions and feedback.

Fields:

* id
* student_id
* assignment_id
* submission_text
* status
* feedback

---

## 8. AI Integration

Google Gemini AI is integrated through a dedicated service layer.

### Assignment Creation

Example:

/ai_assign Assign Hemasri a 500-word essay on AI due on 30 June 2026

Gemini extracts:

* Student Name
* Assignment Title
* Deadline

and automatically creates the assignment.

### Progress Tracking

Example:

/progress I completed 70% of the AI project today

Gemini interprets:

* Progress percentage
* Completion status

### Assignment Review

Example:

/ai_review

Gemini evaluates submitted content and generates:

* Strengths
* Areas for improvement
* Suggested feedback

### Question Answering

Example:

/ask What is Machine Learning?

Gemini generates educational responses for students.

---

## 9. System Workflow

### Teacher Workflow

1. Teacher registers.
2. Teacher creates an assignment.
3. Teacher assigns work to students.
4. Students receive assignment details.
5. Students submit assignment content.
6. Teacher reviews submissions.
7. Teacher provides feedback.
8. Students receive feedback.
9. Dashboards reflect updated status.

### Student Workflow

1. Student registers.
2. Student views assignments.
3. Student submits work.
4. Student receives AI-assisted feedback.
5. Student tracks progress through the dashboard.

---

## 10. Challenges Faced

During development several challenges were encountered:

* Designing the database schema.
* Managing relationships between assignments and submissions.
* Integrating Google Gemini AI.
* Building dashboards using FastAPI and Jinja2.
* Maintaining synchronization between Telegram commands and database updates.
* Testing workflows across multiple users.

---

## 11. Future Enhancements

Potential future improvements include:

* Attendance management system
* Quiz management system
* File upload support
* Multi-teacher support
* Advanced analytics dashboard
* Automated deadline-based reminders
* Cloud deployment
* User authentication and authorization

---

## 12. Conclusion

Classroom Companion successfully demonstrates how AI can be integrated into classroom management workflows.

The project combines conversational interfaces, persistent storage, web dashboards, and generative AI to provide an efficient educational management platform.

The system reduces manual effort for teachers, improves student engagement, and showcases practical applications of prompt engineering and AI-assisted automation.
