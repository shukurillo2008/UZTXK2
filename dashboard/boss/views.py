from django.shortcuts import render, redirect
from main import models
from datetime import datetime
from django.http import HttpResponse

def index_boss(request):
    staff = models.Worker.objects.all().count()
    enter = models.Worker.objects.filter(in_work=True).count()
    not_in_work = models.Worker.objects.filter(in_work=False)
    not_in_work_count = staff - enter

    kitchen = models.Kitchen.objects.last()
    in_kitchen = models.InKitchen.objects.filter(kitchen = kitchen).count()
    context = {
        'workers_count': staff,
        'in_work': enter,
        'not_in_work': not_in_work_count,
        'in_kitchen': in_kitchen,
        'workers':not_in_work
    }
    return render(request, 'boss/index.html', context)


def worker_detail(request, pk):
    worker = models.Worker.objects.get(pk=pk)
    sections = models.Section.objects.all().order_by('title')
    work_shifts = models.WorkShift.objects.all().order_by('start_time')
    enter_exit = models.EnterExit.objects.filter(worker = worker).order_by('-id')

    context = {
        'sections': sections,
        'worker':worker,
        'work_shifts': work_shifts,
        'enter_exit':enter_exit
    }

    return render(request, 'boss/worker_detail.html', context)


def section_list(request):
    sections_count = models.Section.objects.all().count()
    ctsDic = {}
    for cts in models.Section.objects.all():
        ctsQnt = models.Worker.objects.filter(section=cts).count()
        ctsDic[cts] = ctsQnt

    context = {
        'sections':ctsDic,


    }
    return render(request, 'boss/section_list.html', context)

def section_detail(request,id):
    pass


def create_section_user(request):
    if request.user.is_superuser == True:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            title = request.POST.get('title')
            try:
                user_staff = models.User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username=username,
                    password=password,
                )
                models.Section.objects.create(
                    boss = user_staff,
                    title = title
                )
                return redirect('create_section_url')
            except: 
                return HttpResponse('Some thing went wrong =(')
        else:
            return render(request, 'boss/section_create.html')
    else:
        return HttpResponse('You are not super admin')
    

def section_update(request, id):
    section = models.Section.objects.get(id=id)
    if request.user.is_superuser == True or section.boss == request.user:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            title = request.POST.get('title')
            section.boss.first_name = first_name
            section.boss.last_name = last_name
            section.boss.username = username
            section.boss.password = password
            section.title = title
            section.save()
            return render(request, 'section_update.html')
        else:
            return render(request, 'section_detail.html',  context={'section': section})
    else:
        return HttpResponse('You have not access!')


def section_delate(request, id):
    section_delate = models.Section.objects.get(id=id)
    if request.user.is_superuser == True or section_delate.boss == request.user:
        section_delate.delete()
    else:
        return HttpResponse('You have not access!')
    return redirect('list_sections')