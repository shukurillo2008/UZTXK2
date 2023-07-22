from django.shortcuts import render, redirect
from main import models
from datetime import datetime

def index(request):
    section = models.Section.objects.get(boss=request.user)
    worker_count = models.Worker.objects.filter(section = section).count()
    in_work = models.EnterExit.objects.filter(worker__section = section, exit_time__isnull = True).count()
    not_in_work = models.Worker.objects.filter(section = section, in_work = False)
    not_in_work_count = worker_count - in_work

    context = {
        'section': section,
        'workers_count': worker_count,
        'in_work': in_work,
        'not_in_work': not_in_work_count,
        'workers':not_in_work
    }
    
    return render(request, 'sectionboss/index.html', context)

def enter(request):
    worker_id = request.POST.get('worker_id')
    worker = models.Worker.objects.get(id=worker_id)
    enter = models.EnterExit.objects.create(
        worker=worker,
        enter_time=datetime.now(),
    )
    enter.save()
    return redirect('index_url')


def worker_list(request):
    section = models.Section.objects.get(boss = request.user)
    workers = models.Worker.objects.filter(section = section)

    context = {
        'boss': request.user,
        'workers':workers,
    }

    return render(request, 'sectionboss/worker_list.html', context)


def enter_exit(request):
    worker_id = request.POST.get('worker_id')
    worker = models.Worker.objects.get(id=worker_id)

    if worker.in_work:
        exit = models.EnterExit.objects.get(worker=worker, exit_time__isnull=True)
        exit.exit_time = datetime.now()
        exit.save()
        return redirect('workers_list_url')
    
    enter = models.EnterExit.objects.create(
        worker=worker,
        enter_time=datetime.now(),
    )
    enter.save()
    return redirect('workers_list_url')


def worker_detail(request, id):
    worker = models.Worker.objects.get(id=id)
    sections = models.Section.objects.all().order_by('title')
    work_shifts = models.WorkShift.objects.all().order_by('start_time')
    enter_exit = models.EnterExit.objects.filter(worker = worker).order_by('-id')

    context = {
        'sections': sections,
        'worker':worker,
        'work_shifts': work_shifts,
        'enter_exit':enter_exit
    }

    return render(request, 'sectionboss/worker_detail.html', context)

    
