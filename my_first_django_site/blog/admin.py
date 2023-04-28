from django.contrib import admin
from .models import Post, Comment, Category

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    
    autocomplete_fields = ['author']
    list_display = ('title', 'image', 'slug', 'author', 'category', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'category', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('name',)
    search_fields = ('name',)
    
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)