from django.db import models
from users.models import Client, Instructor
from workouts.models import Group, WorkoutType

class GroupEnrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_status = models.CharField(max_length=50, default='paid')

    def __str__(self):
        return f"{self.client} записан в {self.group}"

class IndividualSession(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE)
    session_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='scheduled')

    def __str__(self):
        return f"Индивидуальная {self.client} у {self.instructor}"
