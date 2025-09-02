from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.profile_model import Profile 


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProfileSerializer(serializers.ModelSerializer):
    
    user = BasicUserSerializer(read_only=True)
    

    follows = serializers.SerializerMethodField()
    followed_by = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'user',
            'profile_picture',
            'follows',
            'followed_by',
            'follows_count', 
            'followed_by_count' 
        )
    
    def get_follows(self, obj):
        profiles_followed = obj.follows.all()
        users = [profile.user for profile in profiles_followed]
        return BasicUserSerializer(users, many=True).data

    def get_followed_by(self, obj):
        profiles_followers = obj.followed_by.all()
        users = [profile.user for profile in profiles_followers]
        return BasicUserSerializer(users, many=True).data

    # Adiciona campos de contagem para facilitar a vida do frontend
    def get_follows_count(self, obj):
        return obj.follows.count()

    def get_followed_by_count(self, obj):
        return obj.followed_by.count()
    
    from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from ..models.profile_model import Profile

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