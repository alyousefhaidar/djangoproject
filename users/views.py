
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .models import User, Question, Answer
from .forms import StudentSignUpForm, TeacherSignUpForm, LoginForm, QuestionForm, AnswerForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import student_required, teacher_required
# Create your views here.

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'users/student_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('student-home')
    

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'users/teacher_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teacher-home')
    

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_student:
                return reverse('student-home')
            elif user.is_teacher:
                return reverse('teacher-home')
        else:
            return reverse('login')
    


@login_required
@student_required
def student_home(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'users/student_home.html', context)

@login_required
@teacher_required
def teacher_home(request):
    questions = Question.objects.filter(teacher=request.user.teacher)
    context = {
        'questions': questions
    }
    return render(request, 'users/teacher_home.html', context)


@login_required
@teacher_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.teacher = request.user.teacher
            question.save()
            return redirect('teacher-home')
    else:
        form = QuestionForm()
    return render(request, 'users/create_question.html', {'form': form})

@login_required
@student_required
def create_answer(request, question_id):
    question = Question.objects.get(id=question_id)
    if Answer.objects.filter(question=question, student=request.user.student).exists():
        return redirect('student-home')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.student = request.user.student
            answer.question = question
            answer.save()
            return redirect('student-home')
    else:
        form = AnswerForm()
    return render(request, 'users/create_answer.html', {'form': form, 'question': question})


@login_required
@student_required
def student_question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    if Answer.objects.filter(question=question, student=request.user.student).exists():
        answer = Answer.objects.get(question=question, student=request.user.student)
        answered = True
    else:
        answer = None
        answered = False
    context = {
        'question': question,
        'answer': answer,
        'answered': answered
    }
    return render(request, 'users/student_question_detail.html', context)
@login_required 
@teacher_required
def teacher_question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    if question.teacher != request.user.teacher:
        return redirect('teacher-home')
    answers = Answer.objects.filter(question=question)
    context = {
        'question': question,
        'answers': answers
    }
    return render(request, 'users/teacher_question_detail.html', context)

