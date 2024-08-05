"""Models for client application."""

from django.db import models


class Client(models.Model):
    """Client model."""

    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=18)
    gender = models.CharField(
        max_length=2,
        choices=[('M', 'Male'), ('F', 'Female'), ('Ot', 'Other')],
        default='M'
    )
    address = models.TextField(max_length=500)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        """Convert object to String."""
        return 'name({})_email({})_phone({})'.format(
            self.name,
            self.email,
            self.phone_number
        )

    objects = models.Manager()


class MaleMeasurements(models.Model):
    """Male Measurements model."""

    unit = models.CharField(
        max_length=3,
        choices=[('cm', 'Centimetre'), ('inc', 'Inches')],
        default='inc'
    )
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    shoulder = models.PositiveSmallIntegerField()
    armscye = models.PositiveSmallIntegerField()
    chest = models.PositiveSmallIntegerField()
    bust = models.PositiveSmallIntegerField()
    waist = models.PositiveSmallIntegerField()
    arm_length = models.PositiveSmallIntegerField()
    hips = models.PositiveSmallIntegerField()
    ankle = models.PositiveSmallIntegerField()
    neck = models.PositiveSmallIntegerField()
    back_width = models.PositiveSmallIntegerField()
    inseam = models.PositiveSmallIntegerField()
    wrist = models.PositiveSmallIntegerField()
    crutch_depth = models.PositiveSmallIntegerField(blank=True)
    waist_to_knee = models.PositiveSmallIntegerField(blank=True)
    knee_line = models.PositiveSmallIntegerField(blank=True)
    biceps = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        """Convert object to String."""
        return 'shoulder({})_chest({})_inseam({})'.format(
            self.shoulder,
            self.chest,
            self.inseam
        )
    objects = models.Manager()


class FemaleMeasurements(models.Model):
    """Female Measurements model."""

    unit = models.CharField(
        max_length=3,
        choices=[('cm', 'Centimetre'), ('inc', 'Inches')],
        default='inc'
    )
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    shoulder = models.PositiveSmallIntegerField()
    chest = models.PositiveSmallIntegerField()
    bust = models.PositiveSmallIntegerField()
    waist = models.PositiveSmallIntegerField()
    hips = models.PositiveSmallIntegerField()
    armscye = models.PositiveSmallIntegerField()
    bust = models.PositiveSmallIntegerField()
    arm_length = models.PositiveSmallIntegerField()
    ankle = models.PositiveSmallIntegerField()
    neck = models.PositiveSmallIntegerField()
    back_width = models.PositiveSmallIntegerField()
    inseam = models.PositiveSmallIntegerField()
    wrist = models.PositiveSmallIntegerField()
    front_sh_to_waist = models.PositiveSmallIntegerField(blank=True)
    crutch_depth = models.PositiveSmallIntegerField(blank=True)
    waist_to_knee = models.PositiveSmallIntegerField(blank=True)
    waist_to_hip = models.PositiveSmallIntegerField(blank=True)
    knee_line = models.PositiveSmallIntegerField(blank=True)
    top_arm = models.PositiveSmallIntegerField(blank=True)
    body_rise = models.PositiveSmallIntegerField(blank=True)
    waist_to_floor = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        """Convert object to String."""
        return 'shoulder({})_chest({})_inseam({})'.format(
            self.shoulder,
            self.chest,
            self.inseam
        )
    objects = models.Manager()
