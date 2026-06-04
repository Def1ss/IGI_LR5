from django.db import models
from users.models import Instructor, Client

class WorkoutType(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price_per_session = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_cycle = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, default='group')

    def __str__(self):
        return self.name

class GymHall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    equipment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=150)
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE)
    instructors = models.ManyToManyField(Instructor)
    clients = models.ManyToManyField(Client, blank=True)

    def __str__(self):
        return f"Группа {self.name} ({self.workout_type})"

class ScheduledClass(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    hall = models.ForeignKey(GymHall, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    instructor_ids = models.ManyToManyField(Instructor)

    def __str__(self):
        return f"{self.group} в {self.start_time}"
