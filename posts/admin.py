from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'title', 'slug', 'moderation_status']
    list_editable = ['moderation_status']
    list_per_page = 20


class CommentAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'user', 'content']
    list_editable = ['content']
    list_per_page = 20


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
