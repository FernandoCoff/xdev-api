from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, 
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user_request = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = 'Não foi possível fazer o login com as credenciais fornecidas.'
                raise serializers.ValidationError(msg, code='authorization')

            user = authenticate(request=self.context.get('request'),
                                username=user_request.username,
                                password=password)

            if not user:
                msg = 'Não foi possível fazer o login com as credenciais fornecidas.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'É necessário incluir "email" e "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs