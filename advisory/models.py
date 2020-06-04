from django.db import models

ONE = "Low"
TWO = "Medium"
THREE = "High"

critical = (
    (ONE, "Low"),
    (TWO, "Medium"),
    (THREE, "High"),
)

class ADVISORY(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    criticality = models.CharField(max_length=8, choices = critical)

    def __str__(self):
        return self.description