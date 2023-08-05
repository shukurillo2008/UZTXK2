from django.shortcuts import render, redirect
from main import models
from django.contrib.auth.decorators import login_required

def index(request):
    kitchen = models.Kitchen.objects.last()
    in_kitchen = models.InKitchen.objects.filter(kitchen=kitchen)
    in_work = models.Worker.objects.filter(in_work = True).count()
    workers_count = in_kitchen.count()
    not_in_kitchen = in_work - workers_count

    context = {
        'in_work': in_work,
        'in_kitchen': in_kitchen,
        'workers_count': workers_count,
        'not_in_kitchen': not_in_kitchen
    }

    return render(request, 'kitchen/index.html', context)


@login_required(login_url='login_url')
def kitchen_create(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        worker_shift = request.POST.get('work_shift')
        models.Kitchen.objects.create(
            date = date,
            worker_shift = models.WorkShift.objects.get(id = worker_shift)
        )
    
        return redirect('kitchen_create_url')
    else:
        worker_shift = models.WorkShift.objects.all()
        context = {
            'work_shifts': worker_shift
        }
        return render(request, 'kitchen/kitchen_create.html', context)