from django.contrib import admin
# Register your models here.
from .models import Admin, Authors, BlackList, Book, BookAuthors, BookTypes, Comments, OrderItems, Orders, UserInfo

admin.site.register(Admin)
admin.site.register(Authors)
admin.site.register(BlackList)
admin.site.register(Book)
admin.site.register(BookAuthors)
admin.site.register(BookTypes)
admin.site.register(Comments)
admin.site.register(OrderItems)
admin.site.register(Orders)
admin.site.register(UserInfo)

