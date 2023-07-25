from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Section(models.Model):
    boss = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class WorkShift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f"{self.start_time} -- {self.end_time}"


class Worker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='worker_images/')
    worker_shift = models.ForeignKey(WorkShift, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    in_work = models.BooleanField(default=False)
    nfc = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class EnterExit(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    enter_time = models.DateTimeField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.worker.first_name

    @property
    def status(self):
        if self.enter_time and self.exit_time:
            return False
        return True


class Kitchen(models.Model):
    date = models.DateField()
    worker_shift = models.ForeignKey(WorkShift, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.date}"
    

class InKitchen(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.SET_NULL, null=True)
    Worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.kitchen.date} {self.Worker.first_name}"
    

@receiver(post_save, sender=EnterExit)
def update_worker_status(sender, instance, **kwargs):
    worker = instance.worker
    if instance.enter_time and instance.exit_time:
        worker.in_work = False
    else:
        worker.in_work = True
    worker.save()
    