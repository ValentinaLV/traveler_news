from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from markdown import markdown

from user.models import CustomUser
from user.utils import send_email
from .utils import get_slug


class Post(models.Model):
    MODERATION_STATUS = [
        ('1', 'Approve'),
        ('0', 'Decline')
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True, default='../static/images/image_1.jpg')
    slug = models.SlugField(max_length=150, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    moderation_status = models.CharField(max_length=50, choices=MODERATION_STATUS, default='0')

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = get_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post-details', kwargs={'slug': self.slug})

    def get_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.user} {self.content}"

    def save(self, *args, **kwargs):
        if not self.id:
            send_email(f"Comment was added to your post {self.post.title}",
                       f"Username: {self.user.username}\n"
                       f"Email: {self.user.email}\n"
                       f"Comment body: {self.content}",
                       [self.post.author.email])
        super().save(*args, **kwargs)
