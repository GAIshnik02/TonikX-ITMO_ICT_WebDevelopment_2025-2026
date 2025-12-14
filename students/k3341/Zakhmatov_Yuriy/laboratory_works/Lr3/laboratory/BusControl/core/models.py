from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

class BusType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Bus(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    bus_type = models.ForeignKey(BusType, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.registration_number


class Route(models.Model):
    number = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=200)
    end_point = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_minutes = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.number}: {self.start_point} – {self.end_point}"


class DriverClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Driver(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    driver_class = models.ForeignKey(DriverClass, on_delete=models.PROTECT)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def salary(self):
        return self.driver_class.base_salary * (1 + self.experience_years * Decimal(0.05))


class WorkShift(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    absence_reason = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Причина, если автобус не вышел на линию",
    )

    class Meta:
        unique_together = ("driver", "date", "start_time")

    def __str__(self):
        return f"{self.driver} – {self.route} ({self.date})"
