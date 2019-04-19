from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()

        # we can always add more fields
        fields = ('email', 'password', 'name')

        # allows us to configure a few extra settings in our model serializer
        # ensure that the password is write-only and the minimum length
        # is 5 characters
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        def create(self, validated_data):
            """Creates a new user with encrypted password and return it"""
            return get_user_model().objects.create_user(**validated_data)

        def update(self, instance, validated_data):
            """Update a user,setting the password correctly and return it"""
            password = validated_data.pop('password', None)
            # super will make use of the default update function
            # which we extend here
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()

            return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # Any field that is made from the serializer
    # is passed as attrs in the validate function
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # whenever we override the validate function
        # we must return the values at the end
        attrs['user'] = user
        return attrs
