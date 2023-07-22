from django.shortcuts import render, redirect
from main import models
from datetime import datetime

def index_boss(request):
    staff = models.Worker.objects.all().count()
    enter = models.Worker.objects.filter(in_work=True).count()
    not_in_work = models.Worker.objects.filter(in_work=False)
    not_in_work_count = staff - enter

    tuday = datetime.now()
    kitchen = models.Kitchen.objects.get(date=tuday)
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


