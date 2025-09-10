from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password

# Em users/serializers/register_serializer.py

from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password

# Em users/serializers/register_serializer.py

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
        # Valida se as senhas são idênticas
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password2": "As senhas não são idênticas."})
        
        # --- CORREÇÃO APLICADA AQUI ---
        # Cria uma instância temporária do usuário SEM o campo 'password2'
        # para passar ao validador de senha.
        temp_user_data = attrs.copy()
        temp_user_data.pop('password2', None) # Remove 'password2' da cópia
        temp_user = User(**temp_user_data) # Cria o usuário temporário

        try:
            # Agora passamos o usuário temporário SEM o password2
            validate_password(attrs['password'], user=temp_user)
        except serializers.ValidationError as e:
            # Captura os erros de força da senha e os retorna
            raise serializers.ValidationError({"password": list(e.messages)})
        # --- FIM DA CORREÇÃO ---

        return attrs

    def create(self, validated_data):
        # Remove o campo virtual 'password2' antes de criar o usuário final
        validated_data.pop('password2')
        
        # Chama o método 'create_user' que criptografa a senha
        user = User.objects.create_user(**validated_data)
        
        return user