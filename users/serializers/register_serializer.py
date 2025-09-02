from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'id': {'read_only': True}, 
            'password': {'write_only': True}, 
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "Email já cadastrado!"
                    )
                ]
            },
            'username': {
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "Nome de usuário indisponível."
                    )
                ]
            }
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não são idênticas."})
        try:
            validate_password(attrs['password'], user=User(**attrs))
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):

        validated_data.pop('password2')
        
        user = User.objects.create_user(**validated_data)
        
        return user