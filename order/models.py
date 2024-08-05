"""Models for order application."""

from django.db import models

from client.models import Client
from employee.models import Employee
from product.models import Product


class Order(models.Model):
    """Order model."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, default=None, null=True, on_delete=models.CASCADE)

    RECIEVED, IN_PROGRESS, DELIVERED, CLOSED = 'R', 'I', 'D', 'C'
    ORDER_STATUS_CHOICES = [(RECIEVED, 'Recieved'), (IN_PROGRESS, 'In Progress'),
                            (DELIVERED, 'Delivered'), (CLOSED, 'Closed')]

    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS_CHOICES,
        default=RECIEVED
    )
    payment_status = models.BooleanField(default=False)
    payment_amount = models.PositiveSmallIntegerField()
    advance_payment_amount = models.PositiveSmallIntegerField(default=0, blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    date_recieved = models.DateField(auto_now_add=True)
    order = models.CharField(max_length=50)
    instructions = models.TextField(max_length=500, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        """Convert object to String."""
        return 'Id:{} - DeliveryDate:{} - ClientName:{}'.format(
            self.id,
            self.delivery_date,
            self.client.name
        )


class Task(models.Model):
    """Task Model."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)

    CREATED, IN_PROGRESS, COMPLETED = 'CR', 'I', 'C'
    TASK_STATUS_CHOICES = [(CREATED, 'Created'), (IN_PROGRESS, 'In Progress'), (COMPLETED, 'Completed')]

    status = models.CharField(max_length=2, choices=TASK_STATUS_CHOICES, default=CREATED)
    deadline = models.DateField()
    objects = models.Manager()

    def __str__(self):
        """Convert object to String."""
        return 'OrderId:{} - EmployeeName:{} - Deadline:{} - Task:{}'.format(
            self.order_id.id,
            self.employee_id.name,
            self.deadline,
            self.description
        )
