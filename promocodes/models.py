from django.db import models

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    valid_to = models.DateField()
    applicable_to = models.CharField(max_length=100, default='all')

    def __str__(self):
        return f"Промокод {self.code} ({self.discount_percent}%)"
