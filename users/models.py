"""
Modelos para el módulo de usuarios
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser de Django.
    
    Atributos:
        role (CharField): Rol del usuario en el sistema
    """
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('DESIGN', 'Diseñador'),
        ('CUT', 'Corte'),
        ('PRODUCTION', 'Producción'),
        ('PACKAGING', 'Empaquetado'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='PRODUCTION',
        verbose_name='Rol del Usuario'
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['first_name', 'last_name']
