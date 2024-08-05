"""Models for product appliction."""

import os

from django.db import models
from django.dispatch import receiver
from django.forms.models import model_to_dict


class Product(models.Model):
    """Product model."""

    title = models.CharField(max_length=30, unique=True)
    product_type = models.CharField(max_length=30)
    price = models.PositiveSmallIntegerField()
    date_added = models.DateField(auto_now_add=True)
    stock = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        """Convert product object to string."""
        return 'Title:{} - Price:{} - Stock:{}'.format(
            self.title,
            self.price,
            self.stock
        )


class ProductImages(models.Model):
    """Product image model."""

    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    image1 = models.ImageField(max_length=500, upload_to='images/')
    image2 = models.ImageField(null=True, blank=True, max_length=500, upload_to='images/')
    image3 = models.ImageField(null=True, blank=True, max_length=500, upload_to='images/')
    image4 = models.ImageField(null=True, blank=True, max_length=500, upload_to='images/')
    image5 = models.ImageField(null=True, blank=True, max_length=500, upload_to='images/')

    objects = models.Manager()


@receiver(models.signals.post_delete, sender=ProductImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete file from filesystem when corresponding `ProductImages` object is deleted."""
    model_dict = model_to_dict(instance)
    model_dict.pop('id')
    model_dict.pop('product')
    for k, v in model_dict.items():
        if v:
            if os.path.isfile(v.path):
                os.remove(v.path)


@receiver(models.signals.pre_save, sender=ProductImages)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Delete old file from filesystem when corresponding `ProductImages` object is updated with new file."""
    if not instance.id:
        return False

    try:
        old_instance = ProductImages.objects.get(id=instance.id)
    except ProductImages.DoesNotExist:
        return False

    old_instance_dict = model_to_dict(old_instance)
    old_instance_dict.pop('id')
    old_instance_dict.pop('product')
    new_instance_dict = model_to_dict(instance)
    for k, v in old_instance_dict.items():
        if v:
            if not v == new_instance_dict.get(k):
                if os.path.isfile(v.path):
                    os.remove(v.path)
