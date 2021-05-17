from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book
import csv


# Create your views here.

def all_book(request):
    all_book = Book.objects.filter(is_active=True)
    return render(request, 'bookstore/all_book.html', locals())


def update_book(request, book_id):
    # bookstore/update_book/1
    try:
        book = Book.objects.get(id=book_id, is_active=True)
    except Exception as e:
        print('--update book error is %s' % (e))
        return HttpResponse('This book is not existed')

    if request.method == 'GET':
        return render(request, 'bookstore/update_book.html', locals())

    elif request.method == 'POST':
        price = request.POST['price']
        market_price = request.POST['market_price']
        # 修改数据
        book.price = price
        book.market_price = market_price
        # 保存数据
        book.save()
        return HttpResponseRedirect('/bookstore/all_book')  # 302跳转到all_book首页


def delete_book(request):
    """进行伪删除"""
    # 通过获取查询字符串book_id拿到要删除的book的id
    book_id = request.GET.get('book_id')
    # print(book_id)
    if not book_id:
        return HttpResponse('---请求异常---')
    try:
        book = Book.objects.get(id=book_id, is_active=True)
    except Exception as e:
        print('----delete book get error %s' % (e))
        return HttpResponse('----This book id is error')

    # 将其is_active改为False
    book.is_active = False
    book.save()

    # 302跳转至all_book
    return HttpResponseRedirect('/bookstore/all_book/')


def add_book(request):
    if request.method == 'GET':
        return render(request, 'bookstore/add_book.html')
    if request.method == 'POST':
        title = request.POST['title']
        pub = request.POST['pub']
        price = request.POST['price']
        market_price = request.POST['market_price']

        Book.objects.create(title=title, pub=pub, price=price, market_price=market_price)
        return HttpResponseRedirect('/bookstore/all_book/')


def test1_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="text1.csv"'
    all_book = Book.objects.all()
    writer = csv.writer(response)
    writer.writerow(['id', 'title'])
    for b in all_book:
        writer.writerow([b.id, b.title])
    return response


def page_view(request):
    page_num = request.GET.get('page', 1)
    all_book = Book.objects.filter(is_active=True)
    paginator = Paginator(all_book, 5)  # 初始化paginator
    # 初始化具体页码的page对象
    c_page = paginator.page(int(page_num))
    return render(request, 'bookstore/page_view.html', locals())