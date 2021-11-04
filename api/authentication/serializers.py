from rest_framework import serializers

from .validators import ConfirmationCodeValidator, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code',)
        validators = [ConfirmationCodeValidator()]
