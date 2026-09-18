from django.db import models


class Destination(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    description = models.TextField()
    best_time = models.CharField(max_length=100)
    average_budget = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.state}"