from django.contrib.auth.models import User
from rest_framework import serializers, validators

class RegisterSerializer(serializers.ModelSerializer):
    # Campo para confirmação de senha. Não será salvo no banco de dados.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        # Lista de campos que serão usados para o registro e retornados na resposta.
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'id': {'read_only': True}, # O ID será apenas para leitura
            'password': {'write_only': True}, # A senha principal não será retornada
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
        """
        Este método é chamado para validar os dados do serializer.
        Vamos usá-lo para comparar as senhas.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não são idênticas."})
        return attrs

    def create(self, validated_data):
        """
        Este método é chamado quando a validação passa e um novo usuário
        precisa ser criado.
        """
        # Removemos o campo 'password2' pois ele não existe no modelo User
        validated_data.pop('password2')
        
        # Usamos **validated_data para passar os argumentos para create_user
        user = User.objects.create_user(**validated_data)
        
        return user