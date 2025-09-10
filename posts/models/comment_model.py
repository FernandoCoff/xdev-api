from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .post_model import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comentário de {self.author.username} no post {self.post.id}'
    
    def get_display_time(self):
        now = timezone.now()
        diff = now - self.created_at

        if diff.days == 0 and diff.seconds < 60:
            return "agora"
        if diff.days == 0 and diff.seconds < 3600:
            return f"{diff.seconds // 60} M"
        if diff.days == 0:
            return f"{diff.seconds // 3600} H"
        if diff.days < 30:
            return f"{diff.days} D"
        if diff.days < 365:
            return f"{diff.days // 30} Me"
        return f"{diff.days // 365} A"
