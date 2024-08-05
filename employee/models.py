"""Models for employee application."""

from django.db import models


class Employee(models.Model):
    """Employee model."""

    name = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=2,
        choices=[('M', 'Male'), ('F', 'Female')],
        default='M'
    )
    address = models.TextField(max_length=500)
    phone_number = models.CharField(max_length=15, unique=True)
    joining_date = models.DateField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        """Convert object to String."""
        return 'name:{} - Phone:{} - JoiningDate:{}'.format(
            self.name,
            self.phone_number,
            self.joining_date
        )
