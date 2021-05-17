from django.contrib import admin
from .models import Book, Author


# Register your models here.

class BookManager(admin.ModelAdmin):
    # 列表页显示哪些字段的列
    list_display = ['id', 'title', 'pub', 'price', 'market_price', 'is_active']
    # 控制list_display中字段哪些可以链接到修改页,默认ID
    # list_display_links = ['title']
    # 过滤器
    list_filter = ['pub']
    # 添加搜索框[模糊查询]
    search_fields = ['title']
    # 添加可在列表页编辑的字段
    list_editable = ['price']


class AuthorManager(admin.ModelAdmin):
    list_display = ['id', 'name', 'age']


admin.site.register(Book, BookManager)
admin.site.register(Author, AuthorManager)


