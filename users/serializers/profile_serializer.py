from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from ..models.profile_model import Profile 
from posts.models import Post 


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# 1. Criei um novo serializer específico para as listas de seguidores/seguindo
class FollowListSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir o usuário e a foto de perfil nas listas.
    """
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'profile_picture')


class ProfileSerializer(serializers.ModelSerializer):
    
    user = BasicUserSerializer(read_only=True)

    # Estes campos agora usarão o FollowListSerializer
    follows = serializers.SerializerMethodField()
    followed_by = serializers.SerializerMethodField()
    
    follows_count = serializers.SerializerMethodField()
    followed_by_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'user',
            'profile_picture',
            'follows',
            'followed_by',
            'follows_count', 
            'followed_by_count',
            'is_following',
            'post_count'
        )
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return request.user.profile.follows.filter(pk=obj.pk).exists()

    # 2. Atualizei a função para usar o novo FollowListSerializer
    def get_follows(self, obj):
        profiles_followed = obj.follows.all()
        # Passamos o 'context' para que o serializer tenha acesso ao 'request' se necessário
        return FollowListSerializer(profiles_followed, many=True, context=self.context).data

    # 3. Atualizei esta função também
    def get_followed_by(self, obj):
        profiles_followers = obj.followed_by.all()
        return FollowListSerializer(profiles_followers, many=True, context=self.context).data

    def get_follows_count(self, obj):
        return obj.follows.count()

    def get_followed_by_count(self, obj):
        return obj.followed_by.count()
    
    def get_post_count(self, obj):
        # CORREÇÃO: Revertido para a consulta direta, que é mais robusta.
        return Post.objects.filter(author=obj.user).count()
    

class ProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate(self, attrs):
        if 'password' in attrs or 'password2' in attrs:
            if attrs.get('password') != attrs.get('password2'):
                raise serializers.ValidationError({"password": "As senhas não são idênticas."})
            
            validate_password(attrs['password'], user=self.context['request'].user)

        return attrs

    def update(self, instance, validated_data):
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()
        return instance

class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_picture',)

