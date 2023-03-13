from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    extra = 3


class TitleAdmin(admin.ModelAdmin):
    '''Настраиваем отображение модели в интерфейсе админки'''
    list_display = ('pk', 'name', 'year', 'category', 'description')
    list_editable = ('category',)
    inlines = (
        GenreInline,
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
