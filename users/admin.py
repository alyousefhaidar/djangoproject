
# Register your models here.
#admin admin@site.com red123

from django.contrib import admin
from .models import User, Question, Answer, Student, Teacher

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(Teacher)