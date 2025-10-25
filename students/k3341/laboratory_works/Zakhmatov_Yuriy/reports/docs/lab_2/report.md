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

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.CharField(max_length=30)
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
        return f"{self.subject.name}: {self.description[:100]}"

    def get_last_submission(self, user):
        """Возвращает последнюю сдачу пользователя для этого задания"""
        return self.submission_set.filter(student=user).order_by('-submitted_at').first()


class Submission(models.Model):
    HOMEWORK_STATUS = [
        ('submitted', '📤 Сдано'),
        ('graded', '✅ Оценено'),
        ('late', '⚠️ Сдано с опозданием'),
        ('not_submitted', '⏳ Не сдано'),
    ]

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=HOMEWORK_STATUS,
        default='not_submitted'
    )

    def save(self, *args, **kwargs):
        # Сначала вызываем родительский save, чтобы установились auto_now_add поля
        super().save(*args, **kwargs)

        # Затем обновляем статус, если нужно
        if self.submitted_at and self.homework.due_date:
            if self.submitted_at.date() > self.homework.due_date:
                self.status = 'late'
            elif self.grade is not None:
                self.status = 'graded'
            elif self.text:
                self.status = 'submitted'
        elif self.grade is not None:
            self.status = 'graded'

        # Сохраняем снова, если статус изменился
        if self._state.adding is False:  # Если объект уже существует
            super().save(update_fields=['status'])

    def __str__(self):
        return f"{self.student.username} - {self.homework.subject.name} ({self.get_status_display()})"
~~~

2. Миграция БД

![img.png](screenshots%2Fimg.png)

3. Создаем админку

```python
from django.contrib import admin
from .models import Subject, Homework, Submission

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'issue_date', 'due_date')
    list_filter = ('subject',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'status', 'grade', 'submitted_at')
    list_filter = ('homework', 'grade', 'status')
    search_fields = ('student__username', 'student__first_name', 'student__last_name')
    list_editable = ('status', 'grade')
    actions = ['delete_old_submissions']

    def delete_old_submissions(self, request, queryset):
        """Удаляет все кроме последних сдач"""
        from django.db.models import Max

        # Находим ID последних сдач для каждого студента и задания
        latest_submissions = Submission.objects.values(
            'student', 'homework'
        ).annotate(
            latest_id=Max('id')
        ).values_list('latest_id', flat=True)

        # Удаляем все кроме последних
        deleted_count = Submission.objects.exclude(
            id__in=latest_submissions
        ).delete()[0]

        self.message_user(request, f"Удалено {deleted_count} старых сдач")

    delete_old_submissions.short_description = "Удалить все кроме последних сдач"
```

4. Создаем представления


