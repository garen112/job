from django.contrib import admin
from .models import Post, Blog

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
    )


admin.site.register(Post)


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
    )
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Blog, BlogAdmin)
