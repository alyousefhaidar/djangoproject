
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='teacher')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

class Question(models.Model):
    question = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(default=timezone.now)

class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(default=timezone.now)

