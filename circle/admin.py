from django.contrib import admin
from .models import PostLike, PostComment, PyPost, PostImage
# Register your models here.


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id',)


class PyPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(PostComment)
admin.site.register(PostImage)
admin.site.register(PyPost, PyPostAdmin)
