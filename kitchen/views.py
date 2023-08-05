from django.shortcuts import render, redirect
from main import models


def index(request):
    kitchen = models.Kitchen.objects.last()
    in_kitchen = models.InKitchen.objects.filter(kitchen=kitchen)
    in_work = models.Worker.objects.filter(in_work = True).count()
    workers_count = in_kitchen.count()
    not_in_kitchen = in_work - workers_count

    context = {
        'in_kitchen': in_kitchen,
        'workers_count': workers_count,
        'not_in_kitchen': not_in_kitchen
    }

    return render(request, 'kitchen/index.html', context)
