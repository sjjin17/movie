from django.contrib import admin
from .models import Review, Comment

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'created_at', 'updated_at', 'star_rate', 'user', 'movie',)


admin.site.register(Review, ReviewAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'review', 'content', 'created_at', 'updated_at',)


admin.site.register(Comment, CommentAdmin)