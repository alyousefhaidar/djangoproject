from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.student_home, name="student-home"),
    path("teacher/", views.teacher_home, name="teacher-home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/student/", views.StudentSignUpView.as_view(), name="student-signup"),
    path("signup/teacher/", views.TeacherSignUpView.as_view(), name="teacher-signup"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("teacher/question/create/", views.create_question, name="create-question"),
    path("question/<int:question_id>/answer/", views.create_answer, name="create-answer"),
    path("question/<int:question_id>/", views.student_question_detail, name="student-question-detail"),
    path("teacher/question/<int:question_id>/", views.teacher_question_detail, name="teacher-question-detail"),
]