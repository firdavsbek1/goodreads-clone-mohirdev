from django.contrib import admin
from .models import Book,Author,BookAuthor,Review
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('title','isbn')
    search_fields = ('title','isbn')


class AuthorAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email',)
    search_fields = ('first_name','email')


class BookAuthorAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(BookAuthor,BookAuthorAdmin)
admin.site.register(Review,ReviewAdmin)