from django.contrib import admin
from . import models

admin.site.register(models.Section)
admin.site.register(models.WorkShift)
admin.site.register(models.Worker)
admin.site.register(models.EnterExit)
admin.site.register(models.Kitchen)
admin.site.register(models.InKitchen)
