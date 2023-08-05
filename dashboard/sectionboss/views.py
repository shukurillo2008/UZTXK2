from django.shortcuts import render, redirect
from main import models
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def paginatorfun(per_page, page_number, list):
    paginator = Paginator(list, per_page)
    try:
        result = paginator.page(page_number)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    
    return result


@login_required(login_url='login_url')
def index(request):
    section = models.Section.objects.get(boss=request.user)
    workers = models.Worker.objects.filter(section=section)
    worker_count = workers.count()
    in_work = workers.filter(in_work = True).count()
    not_in_work_count = worker_count - in_work
    page_number = request.GET.get('page', 1)
    not_in_work = paginatorfun(10, page_number, workers.filter(in_work = False)) 

    context = {
        'section': section,
        'workers_count': worker_count,
        'in_work': in_work,
        'not_in_work': not_in_work_count,
        'workers': not_in_work 
    }

    return render(request, 'sectionboss/index.html', context)


@login_required(login_url='login_url')
def enter(request):
    worker_id = request.POST.get('worker_id')
    worker = models.Worker.objects.get(id=worker_id)
    enter = models.EnterExit.objects.create(
        worker=worker,
        enter_time=datetime.now(),
    )
    enter.save()
    return redirect('index_url')


@login_required(login_url='login_url')
def worker_list(request):
    search = request.GET.get('search')
    section = models.Section.objects.get(boss = request.user)
    if search:
        workers = models.Worker.objects.filter(Q(first_name__icontains=search)|Q(last_name__icontains=search), section = section)
    else:
        workers = models.Worker.objects.filter(section = section)
    page_number = request.GET.get('page', 1)
    workers_page = paginatorfun(10, page_number, workers) 

    context = {
        'section':section,
        'workers':workers_page
    }

    return render(request, 'sectionboss/worker_list.html', context)


@login_required(login_url='login_url')
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


@login_required(login_url='login_url')
def worker_detail(request, id):
    worker = models.Worker.objects.get(id=id)
    sections = models.Section.objects.all().order_by('title')
    work_shifts = models.WorkShift.objects.all().order_by('start_time')
    enter_exit = models.EnterExit.objects.filter(worker = worker).order_by('-id')
    page_number = request.GET.get('page', 1)
    list_page = paginatorfun(6, page_number, enter_exit) 

    if request.user == worker.section.boss or request.user.is_superuser == True:
        context = {
            'sections': sections,
            'worker':worker,
            'work_shifts': work_shifts,
            'enter_exit':list_page
        }

        return render(request, 'sectionboss/worker_detail.html', context)
    return HttpResponse("You have not access =( ")


@login_required(login_url='login_url')
def worker_update(request):
    worker_id = request.POST.get('worker_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    img = request.FILES.get('img')
    section = request.POST.get('section')
    work_shift = request.POST.get('work_shift')
    nfc = request.POST.get('nfc')

    worker = models.Worker.objects.get(id=worker_id)
    if img is not None:
        worker.img = img
    worker.first_name = first_name
    worker.last_name = last_name
    worker.section = models.Section.objects.get(title = section)
    worker.worker_shift = models.WorkShift.objects.get(id = int(work_shift))
    worker.nfc = nfc
    worker.save()

    return redirect('workers_detail_url', worker_id)


def worker_create(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        img = request.FILES.get('img')
        work_shift = request.POST.get('work_shift')
        nfc = request.POST.get('nfc')


        models.Worker.objects.create(
            first_name = first_name,
            last_name = last_name,
            img = img,
            worker_shift = models.WorkShift.objects.get(id = int(work_shift)),
            section = models.Section.objects.get(boss = request.user),
            nfc = nfc
        )
        return redirect('worker_create_url')
    else:
        sections = models.Section.objects.all().order_by('title')
        work_shifts = models.WorkShift.objects.all().order_by('start_time')

        context = {
            'sections': sections,
            'work_shifts': work_shifts
        }

        return render(request, 'sectionboss/worker_create.html', context)


@login_required(login_url='login_url')
def worker_delete(request):
    worker_id = request.POST.get('worker_id')
    worker = models.Worker.objects.get(id=int(worker_id))
    worker.delete()
    return HttpResponse('deleted')
