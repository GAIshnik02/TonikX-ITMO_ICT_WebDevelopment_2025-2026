from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Homework, Submission


# Create your views here.

#регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})


#домашняя страница
@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('register')

    query = request.GET.get('q')
    homeworks = Homework.objects.all().order_by('-due_date')

    if query:
        homeworks = homeworks.filter(
            Q(subject__name__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__teacher__icontains=query)
        )

    paginator = Paginator(homeworks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/home.html', {'page_obj': page_obj})


#отправка задания
@login_required
def submit_homework(request, homework_id):
    homework = Homework.objects.get(id=homework_id)
    if request.method == 'POST':
        text = request.POST.get("text")
        submission = Submission.objects.create(
            homework=homework,
            student=request.user,
            text=text
        )
        return HttpResponseRedirect('/')
    return render(request, 'tasks/submit.html', {'homework': homework})


#отображение оценок
@login_required
def grades(request):
    # Берем только последние сдачи для каждого задания
    from django.db.models import Max
    latest_submissions = Submission.objects.filter(
        student=request.user
    ).values(
        'homework'
    ).annotate(
        latest_id=Max('id')
    ).values_list('latest_id', flat=True)

    submissions = Submission.objects.filter(id__in=latest_submissions)
    return render(request, 'tasks/grades.html', {'submissions': submissions})