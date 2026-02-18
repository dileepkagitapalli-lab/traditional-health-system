from django.db import models
from django.contrib.auth.models import User

class Remedy(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    benefits = models.TextField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
