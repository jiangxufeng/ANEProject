from django.contrib import admin
from .models import PostLike
# Register your models here.


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(PostLike, PostLikeAdmin)