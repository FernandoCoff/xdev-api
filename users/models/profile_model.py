import random # Para escolher a cor
import requests # Para baixar a imagem
from io import BytesIO # Para manipular os dados da imagem em memória

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile 


PASTEL_COLORS = [
    'E6E6FA', 'FFB6C1', 'ADD8E6', 'F08080', '90EE90',
    'FFDAB9', 'B0E0E6', 'FFDEAD', 'DDA0DD', '87CEFA'
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pics',
        null=True,
        blank=True
    )
    
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        username = instance.username
        initial = username[0].upper() if username else 'X'

        
        random_color = random.choice(PASTEL_COLORS)


        placeholder_url = f'https://placehold.co/400x400/{random_color}/FFFFFF?font=poppins&text={initial}'

        try:
            response = requests.get(placeholder_url)
            response.raise_for_status() 

            image_data = BytesIO(response.content)
            file_name = f'{username}_default.png'
            profile.profile_picture.save(file_name, ContentFile(image_data.read()), save=True)

        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar a imagem de perfil para {username}: {e}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()