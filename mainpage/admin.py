from django.contrib import admin
from .models import Book, Food, FoodComment, Application
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'place')


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FoodCommentAdmin(admin.ModelAdmin):
    list_display = ('content',)


admin.site.register(Book, BookAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(FoodComment, FoodCommentAdmin)
admin.site.register(Application)