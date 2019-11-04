from polymorphic.models import PolymorphicModel
from django.db import models


class Configuration(PolymorphicModel):
    description = models.TextField(max_length=255, blank=True, verbose_name='Descripción')
    name = models.CharField(max_length=128, blank=True, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self):
        pass

    def set_description(self, desc):
        self.description = desc

    def set_name(self, name):
        self.name = name

    def apply(self):
        pass
