from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

User = get_user_model()


class ConfirmationCodeValidator:
    message = _('Confirmation code is invalid')

    def __init__(self, message=None):
        self.message = message or self.message

    def __call__(self, serializer):
        username, code = serializer.values()
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, code):
            raise ValidationError(self.message)
