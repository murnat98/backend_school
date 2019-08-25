from django.db import models


class Imports(models.Model):
    pass


class Citizens(models.Model):
    import_id = models.ForeignKey('citizens.Imports', on_delete=models.CASCADE, related_name='import_id')
    citizen_id = models.PositiveIntegerField()
    town = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    building = models.CharField(max_length=256)
    apartment = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    birth_date = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=(('male', 'male'), ('female', 'female')))


class Relatives(models.Model):
    import_id = models.ForeignKey('citizens.Imports', on_delete=models.CASCADE)
    citizen_1_id = models.ForeignKey('citizens.Citizens', on_delete=models.CASCADE, related_name='citizen_1_id')
    citizen_2_id = models.ForeignKey('citizens.Citizens', on_delete=models.CASCADE, related_name='citizen_2_id')
