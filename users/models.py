from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .validators import UsernameMeValidator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, USER,),
        (MODERATOR, MODERATOR,),
        (ADMIN, ADMIN,),
    ]

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[UsernameMeValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    bio = models.TextField(_('bio'), blank=True)
    role = models.CharField(
        _('role'),
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER
    )

    objects = CustomUserManager()

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


@receiver(post_save, sender=User)
def create_user_confirmcode(sender, instance, created, **kwargs):
    if created:
        code = default_token_generator.make_token(instance)
        instance.email_user('Confirmation code', code)
