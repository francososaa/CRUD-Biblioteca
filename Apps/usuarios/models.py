# DJANGO
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 


class UsuarioManager(BaseUserManager):
    def _create_user(self, username, email, nombre, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            nombre = nombre,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self.db)
        return user

    def create_user(self, username, email, nombre, is_staff, password = None, **extra_fields):
        return self._create_user(username, email, nombre, password, is_staff, False, **extra_fields)
    
    def create_superuser(self, username, email, nombre, password = None, **extra_fields):
        return self._create_user(username, email, nombre, password, True, True, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario', max_length=100, unique=True)
    email = models.EmailField('Correo Electronico', max_length=254, unique=True)
    nombre = models.CharField('Nombre', max_length=100, null=False, blank=False)
    apellido = models.CharField('Apellido', max_length=100, blank=True)
    fecha_creacion = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UsuarioManager()

    class Meta:
        verbose_name = 'usuario'  
        verbose_name_plural = 'usuarios'
        ordering = ['id']

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre','apellido']

    def natural_key(self):
        return (self.username)
    
    def __str__(self):
        return f'{self.apellido} {self.nombre}'

    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

        email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

        send_mail(
            # title:
            "Password Reset for {title}".format(title="Some website title"),
            # message:
            email_plaintext_message,
            # from:
            "soosaf22@gmail.com",
            # to:
            [reset_password_token.user.email]
        )

