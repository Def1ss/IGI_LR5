from django.contrib import admin
from .models import (
    WorkoutType,
    GymHall,
    Group,
    ScheduledClass
)

admin.site.register(WorkoutType)
admin.site.register(GymHall)
admin.site.register(Group)
admin.site.register(ScheduledClass)