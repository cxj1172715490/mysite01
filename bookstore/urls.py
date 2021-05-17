from django.urls import path
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/bookstore/all_book/
    path('all_book/', views.all_book),

    path('update_book/<int:book_id>', views.update_book),

    path('delete_book/', views.delete_book),

    path('add_book/', views.add_book),

    # csv文件下载测试
    path('test1_csv/', views.test1_csv),

    path('page_view/', views.page_view),
]
