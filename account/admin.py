from django.contrib import admin
from .models import LoginUser, Follow
# Register your models here.


class LoginUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


admin.site.register(LoginUser, LoginUserAdmin)
admin.site.register(Follow)
# admin.site.register(Fans)
