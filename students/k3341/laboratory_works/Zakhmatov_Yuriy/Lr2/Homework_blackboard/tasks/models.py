from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=30)
    teacher_first_name = models.CharField(max_length=30)
    teacher_last_name = models.CharField(max_length=30)
    teacher_email = models.EmailField()

    def __str__(self):
        return self.name

class Homework(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    penalty_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject: {self.text[:100]}}"

class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.homework.subject.name}"

