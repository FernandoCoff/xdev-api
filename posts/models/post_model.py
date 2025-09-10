from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='liked_posts', 
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post de {self.author.username} em {self.created_at.strftime("%d/%m/%Y")}'

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    def get_display_time(self):
        now = timezone.now()
        delta = now - self.created_at

        if delta < timedelta(minutes=1):
            return f"{delta.seconds} seg"
        elif delta < timedelta(hours=1):
            return f"{delta.seconds // 60} min"
        elif delta < timedelta(days=1):
            return f"{delta.seconds // 3600} H"
        elif delta < timedelta(weeks=1):
            return f"{delta.days} D"
        else:
            return f"{delta.days // 7} S"
