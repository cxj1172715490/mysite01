import os.path

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import time, csv
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from upload_app.models import Content

POST_FORM = '''
<form method='post' action='/test_get_post'>
    用户名:<input type='text' name='uname'>
    <input type='submit' value='提交'>
</form>
'''


def page_2003_view(request):
    html = "<h1>这是第一个页面</h1>"
    return HttpResponse(html)


def index_view(request):
    html = "这是我的首页"
    return HttpResponse(html)


def page1_view(request):
    html = "这是编号为1的网页"
    return HttpResponse(html)


def page2_view(request):
    html = "这是编号为2的网页"
    return HttpResponse(html)


def pagen_view(request, pg):
    html = '这是编号为{}的网页'.format(pg)
    return HttpResponse(html)


def cal_view(request, n, op, m):
    if op not in ['add', 'sub', 'mul']:
        return HttpResponse('Your op is wrong!')
    result = 0
    if op == 'add':
        result = n + m
    elif op == 'sub':
        result = n - m
    elif op == 'mul':
        result = n * m
    return HttpResponse('结果为：{}'.format(result))


def cal2_view(request, x, op, y):
    html = 'x:{},op:{},y:{}'.format(x, op, y)
    return HttpResponse(html)


def birthday_view(request, y, m, d):
    html = '生日为{}年{}月{}日'.format(y, m, d)
    return HttpResponse(html)


def test_get_post(request):
    if request.method == "GET":
        print(request.GET['a'])  # 当有多个值时只取最后一个
        print(request.GET.getlist('a'))  # 获取多个值
        print(request.GET.get('c', 'no c'))  # 有默认值
        return HttpResponse(POST_FORM)
    elif request.method == "POST":
        print('uname is', request.POST['uname'])
        return HttpResponse('post is ok')
    else:
        pass

    return HttpResponse('--test get post is ok--')


def test_html(request):
    # 方案1
    # from django.template import loader
    # t = loader.get_template('test_html.html')  # 通过loader加载模板
    # html = t.render()  # 将t转换成html字符串
    # return HttpResponse(html)  # 用响应对象将转换的字符串内容返回给浏览器

    # 方案2
    from django.shortcuts import render
    dic = {'username': 'chengxinjie', 'age': 20}
    return render(request, 'test_html.html', dic)


def test_if_for(request):
    dic = {}
    dic['x'] = 20
    dic['lst'] = ['Tom', 'Jack', 'Lily']
    return render(request, 'test_if_for.html', dic)


def test_mycal(request):
    if request.method == 'GET':
        return render(request, 'mycal.html')
    elif request.method == "POST":
        # 处理计算
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        op = request.POST['op']

        result = 0
        if op == 'add':
            result = x + y
        elif op == 'sub':
            result = x - y
        elif op == 'mul':
            result = x * y
        elif op == 'div':
            result = x / y

        # dic={'x':x,'y':y,'op':op} 相当于locals()
        return render(request, 'mycal.html', locals())


def base_view(request):
    return render(request, 'base.html')


def music_view(request):
    return render(request, 'music.html')


def sport_view(request):
    return render(request, 'sport.html')


def test_url(request):
    return render(request, 'test_url.html')


def test_url_result(request, age):
    # return HttpResponse('---test url is ok----')

    # 302跳转
    from django.urls import reverse
    url = reverse('base_index')
    return HttpResponseRedirect(url)


def test_static(request):  # 静态文件操作
    return render(request, 'test_static.html')


def set_cookies(request):
    resp = HttpResponse('set cookies is ok')
    resp.set_cookie('uname', 'iu', 500)
    return resp


def get_cookies(request):
    value = request.COOKIES.get('uname')
    return HttpResponse('value is %s' % (value))


def set_session(request):
    request.session['uname'] = 'iu'
    return HttpResponse('set session is ok')


def get_session(request):
    value = request.session.get('iu')
    return HttpResponse('sessoin value is %s' % (value))


@cache_page(15)  # 装饰器 整体缓存
def test_cache(request):
    t = time.time()
    return HttpResponse('t is %s' % (t))


def test_page(request):
    # 利用查询字符串 /test_page?page=1
    page_num = request.GET.get('page', 1)
    all_data = ['a', 'b', 'c', 'd', 'e']
    paginator = Paginator(all_data, 2)  # 初始化paginator
    # 初始化具体页码的page对象
    c_page = paginator.page(int(page_num))
    return render(request, 'test_page.html', locals())


def test_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="text.csv"'
    all_data = ['a', 'b', 'c', 'd']
    writer = csv.writer(response)
    writer.writerow(all_data)
    return response


def make_page_csv(request):
    page_num = request.GET.get('page', 1)
    all_data = ['a', 'b', 'c', 'd', 'e']
    paginator = Paginator(all_data, 2)  # 初始化paginator
    # 初始化具体页码的page对象
    c_page = paginator.page(int(page_num))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="page-%s.csv"' % (page_num)
    writer = csv.writer(response)
    for b in c_page:
        writer.writerow([b])
    return response


def test_upload(request):
    if request.method == 'GET':
        return render(request, 'test_upload.html')
    if request.method == 'POST':
        title = request.POST['title']
        my_file = request.FILES['my_file']
        Content.objects.create(title=title, picture=my_file)
        return HttpResponse('上传文件成功')


@csrf_exempt
def upload_view(request):
    if request.method == 'GET':
        return render(request, 'test_upload.html')
    elif request.method == 'POST':
        a_file = request.FILES('my_file')
        print('上传的文件名是：', a_file.name)
        filename = os.path.join(settings.MEDIA_ROOT, a_file.name)
        with open(filename, 'wb') as f:
            data = a_file.file.read()
            f.write(data)
        return HttpResponse('接收文件：' + a_file.name + '成功')
