from django.contrib import admin

from .models import Post, Comment
from .forms import PostAdminForm



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'author', 'published',)
    list_filter = ('created', 'published')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    # exclude = ['slug']


    


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
    
