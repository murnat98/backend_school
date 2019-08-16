from django.db import models


class Imports(models.Model):
    pass


class Citizens(models.Model):
    import_id = models.ForeignKey(Imports, on_delete=models.CASCADE, related_name='import_id')
    citizen_id = models.PositiveIntegerField()
    town = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    apartment = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=(('m', 'male'), ('f', 'female')))


class Relatives(models.Model):
    import_id = models.ForeignKey(Imports, on_delete=models.CASCADE)
    citizen_1_id = models.ForeignKey(Citizens, on_delete=models.CASCADE, related_name='citizen_1_id')
    citizen_2_id = models.ForeignKey(Citizens, on_delete=models.CASCADE, related_name='citizen_2_id')
