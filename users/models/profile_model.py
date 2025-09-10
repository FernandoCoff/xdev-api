import random 
import requests 
from io import BytesIO 
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile 


PASTEL_COLORS = [
    'E6E6FA', 'FFB6C1', 'ADD8E6', 'F08080', '90EE90',
    'FFDAB9', 'B0E0E6', 'FFDEAD', 'DDA0DD', '87CEFA'
]

def user_profile_picture_path(instance, filename):
    """
    Gera um caminho para o arquivo de foto de perfil, garantindo que seja único.
    Ex: 'profile_pics/username.jpg'
    """
    # Pega a extensão do arquivo (ex: .jpg, .png)
    ext = os.path.splitext(filename)[1]
    # Cria um novo nome de arquivo usando o username do usuário
    new_filename = f"{instance.user.username}{ext}"
    
    # Retorna o caminho completo, ex: 'profile_pics/filister.jpg'
    return os.path.join('profile_pics', new_filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to= user_profile_picture_path,
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
            file_name = f'{username}_default.svg'
            profile.profile_picture.save(file_name, ContentFile(image_data.read()), save=True)

        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar a imagem de perfil para {username}: {e}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()