from django.db import models
from users.models import User


class Car(models.Model):
    plate = models.CharField(max_length=10, blank=False)  # Πινακίδα
    brand = models.CharField(max_length=254, blank=False, verbose_name='Car Brand')
    model = models.CharField(max_length=254, blank=False, verbose_name='Car Model')
    year = models.IntegerField(blank=False, verbose_name='Car Year')
    color = models.CharField(max_length=20, blank=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car')

    class Meta:
        verbose_name = 'Όχημα'
        verbose_name_plural = 'Οχήματα'

    def __str__(self):
        return self.plate

    def get_car_full_details(self):
        return '/'.join([self.plate, self.color, self.brand, self.model, self.year])

    def get_owner(self):
        return self.owner
