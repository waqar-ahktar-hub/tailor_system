"""Utility class for frequently needed functions."""

import random
import string
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from client.models import Client, MaleMeasurements
from employee.models import Employee
from order.models import Order, Task
from product.models import Product, ProductImages
from tms.constants import DUMMY_ADDRESS_MARKER, DUMMY_EMAIL_MARKER, DUMMY_ORDER_MARKER, DUMMY_TASK_MARKER


def get_future_date(days_to_add=5):
    """Return date in future."""
    return datetime.today() + timedelta(days=days_to_add)


class RandomDataGenerator:
    """Functions for creating random strings."""

    def get_random_alpha_string(self, length=5):
        """Generate a random alpha string."""
        random_string = ''.join(random.choices(string.ascii_letters + ' ', k=length))
        return random_string.lower()

    def get_random_address(self, length=10):
        """Generate a random alpha string."""
        random_string = ''.join(random.choices(string.ascii_letters, k=length))
        return random_string

    def get_random_numeric_string(self, length=13):
        """Generate a random numeric string."""
        random_string = ''.join(random.choices(string.digits, k=length))
        return random_string

    def get_n_unique_names(self, n):
        """List of space separated title case strings."""
        i = 0
        name_set = []
        while True and i < n:
            name = self.get_random_alpha_string().title() + ' ' + self.get_random_alpha_string().title()
            if name not in name_set:
                name_set.append(name)
                i += 1
        return name_set

    def get_n_unique_emails(self, n, existing_emails):
        """List of emails."""
        i = 0
        email_set = []
        while True and i < n:
            email = self.get_random_alpha_string() + DUMMY_EMAIL_MARKER
            if (email not in email_set) and (email not in existing_emails):
                email_set.append(email)
                i += 1
        return email_set

    def get_n_unique_numbers(self, n, existing_phones):
        """List of phone numbers."""
        phone_set = []
        i = 0
        while True and i < n:
            phone = '+' + self.get_random_numeric_string()
            if (phone not in phone_set) and (phone not in existing_phones):
                phone_set.append(phone)
                i += 1

        return phone_set

    def get_random_number(self, upper_limit, lower_limit=0):
        """Generate a random number."""
        if upper_limit - lower_limit == 0:
            return 1
        else:
            return random.randrange(lower_limit, upper_limit, 1)


class TestDbSetUp(RandomDataGenerator):
    """Functions needed to set Database for tests."""

    def create_user(self):
        """Create a user."""
        username = 'test_user'
        password = '12345'
        user, p = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()
        return user, username, password

    def create_client(self, email_post_fix='@test.com'):
        """Create a Client."""
        client = Client.objects.create(**{
            'name': 'Jon Snow',
            'age': 18,
            'gender': 'M',
            'address': 'night watch wall',
            'phone_number': '+9290078602',
            'email': '{}{}'.format(self.get_random_alpha_string(), email_post_fix)
        })
        client.save()
        return client

    def create_order(self, client):
        """Create an order."""
        delivery_date = datetime.today() + timedelta(days=5)
        order = Order.objects.create(**{
            'client': client,
            'status': 'I',
            'payment_status': False,
            'payment_amount': 1500,
            'advance_payment_amount': 500,
            'delivery_date': delivery_date.strftime('%Y-%m-%d'),
            'order': DUMMY_ORDER_MARKER,
            'instructions': 'Ban instead of collar.'
        })
        order.save()
        return order

    def create_employee(self):
        """Create employee."""
        employee = Employee.objects.create(**{
            'name': 'Jon Snow',
            'gender': 'M',
            'address': DUMMY_ADDRESS_MARKER,
            'phone_number': '+' + self.get_random_numeric_string(),
        })
        employee.save()
        return employee

    def create_product(self):
        """Create product."""
        product = Product.objects.create(**{
            'title': 'S Afr',
            'product_type': 'Shalwar Kameez',
            'stock': 200,
            'price': 5000,
        })
        product.save()
        return product

    def create_product_images(self, product):
        """Create product."""
        path = settings.BASE_DIR + '/tms/test_image.jpg'
        test_img = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(path, 'rb').read(),
            content_type='image/jpeg'
        )
        product_images = ProductImages.objects.create(**{
            'product': product,
            'image1': test_img
        })
        product_images.save()
        return product_images

    def create_task(self, order, employee):
        """Create task."""
        delivery_date = datetime.today() + timedelta(days=5)
        task = Task.objects.create(**{
            'order': order,
            'employee': employee,
            'status': 'I',
            'description': DUMMY_TASK_MARKER,
            'deadline': delivery_date.strftime('%Y-%m-%d'),
        })
        task.save()
        return task

    def create_male_measurements(self, client):
        """Create male measurement model."""
        measurements = MaleMeasurements.objects.create(**{
            'client': client,
            'unit': 'cm',
            'shoulder': 12,
            'armscye': 12,
            'chest': 12,
            'bust': 12,
            'waist': 12,
            'arm_length': 12,
            'hips': 12,
            'ankle': 12,
            'neck': 12,
            'back_width': 12,
            'inseam': 12,
            'wrist': 12,
            'crutch_depth': 12,
            'waist_to_knee': 12,
            'knee_line': 12,
            'biceps': 12,

        })
        measurements.save()
        return measurements
