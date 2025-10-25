# Лабораторная работа 2

---

## Реализация простого сайта средствами DJANGO

**Цель**: Овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2.

**Практическое задание:** Реалищовать сайт используя фреймворк Django 3 и СУБД PostgreSQL *, в соответствии с вариантом задания лабораторной работы.

**Вариант:** 2 (8 номер в журнале)

**Доска домашних заданий.**

О домашнем задании должна храниться следующая информация: предмет,
преподаватель, дата выдачи, период выполнения, текст задания, информация о штрафах.
Необходимо реализовать следующий функционал:

* Регистрация новых пользователей.
* Просмотр домашних заданий по всем дисциплинам (сроки выполнения, описание задания).
* Сдача домашних заданий в текстовом виде.
* Администратор (учитель) должен иметь возможность поставить оценку за задание средствами Django-admin.
* В клиентской части должна формироваться таблица, отображающая оценки
всех учеников класса.

---
 
## Выполнение работы

1. Создание БД нашего сайта:

~~~python
from django.db import models
from django.contrib.auth.models import User

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
~~~

2. Миграция БД

![img.png](screenshots%2Fimg.png)

3. 
