#### 创建数据库

```mysql
create database note_project default charset utf8;
```



#### 模板的继承

不重写，将按照父模板的效果显示；重写，则按照重写效果显示。

继承模板extends标签（写在模板文件的第一行）

例如 {% extends 'base.html' %}

子模版 重写父模板中的内容块

```html
{% block bolck_name %}
子模块用来覆盖父模板中block_name块的内容
{% endblock block_name %}
```

模板继承时，服务器端的动态内容无法继承



#### url反向解析

**path函数的语法**

path(route,views,name="别名")

path('page',views.page_view,name="page_url")

通过url标签实现地址的反向解析

{% url  ’别名‘  %}
{% url  '别名’  ‘参数值1’  '参数值2' %}

```html
{% url 'pagen' '400' %}
{% url 'person' age='18' name='gxn' %}
```

在视图函数中可调用django中的reverse方法进行反向解析

```python
from django.urls import reverse
reverse('别名',args=[],kwargs={})
ex:
print(reverse('pagen',args=[300]))
print(reverse('person',kwargs={'name':'zhangsan','age':20}))
```



#### 访问静态文件

在settings.py文件中配置静态文件

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**绝对路径、相对路径、static标签三种方法访问静态文件**

通过{% static %}标签访问静态文件

1、加载static - {% load static %}

2、使用静态资源 - {% static '静态资源路径' %}

3、样例

```html
<img src={% static 'image/iu.jpg' %}>
```



#### 应用

创建应用

```python
python manage.py startapp music
```

在settings.py的INSTALLED_APPS列表中配置安装此应用



#### 分布式路由

配置：

1、主路由中调用include函数，用于将当前路由转到各个应用的路由配置文件的urlpatterns进行分布式处理。

```python
include('app名字.url模块名')
```

2、应用下配置urls.py，手动创建，内容结构与主路由完全一样



应用下的模板

1、应用下手动创建templates文件夹

2、settings.py中开启应用模板功能



#### 模型层及ORM框架

创建数据库

进入mysql数据库执行：

​	create database 数据库名 default charset utf8

```mysql
create database mysite01 default charset utf8;
```

​	通常数据库名跟项目名保持一致

settings.py里进行数据库配置

​	修改DATABASES配置项的内容，由sqlite3变为mysql

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite01',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
```

模型是一个python类，它是由django.db.models.Model派生出的子类

```python
from django.db import models
class Book(models.Model):
    title = models.CharField('书名', max_length=50, default='')
    price = models.DecimalField('价格', max_digits=7, decimal_places=2)
```

ORM即对象关系引射，避免使用sql语句操作数据库

| ORM  |   DB   |
| :--: | :----: |
|  类  | 数据表 |
| 对象 | 数据行 |
| 属性 |  字段  |

**数据库迁移**

​	1、生成迁移文件-执行python manage.py makemigrations

​	2、执行迁移脚本程序- 执行python manage.py migrate

**常用字段类型**

|     django      |    mysql     |
| :-------------: | :----------: |
| Boolean Field() |   tinyint    |
|   CharField()   |   varchar    |
|   DateField()   |     date     |
| DateTimeField() | datetime(6)  |
|  FloatField()   |    double    |
| DecimalField()  | decimal(x,y) |
|  EmailField()   |   varchar    |
| IntegerField()  |     int      |
|  ImageField()   | varchar(100) |
|   TextField()   |   longtext   |

**模型类-Meta类**

使用Meta类来给模型赋予属性

```python
class Book(models.Model):
	...
    class Meta:
        db_table = 'book'  # 修改表名
```

**创建数据**

1、objects对象管理器

```python
class MyModel(models.Model):
    ...
MyModel.objects.create(...)  # objects是管理器对象

from bookstore.models import Book
b1 = Book.objects.create(title='Python',pub='清华大学出版社',price=20,market_price=25)
```

2、创建MyModel实例对象，并调用save()进行保存

```python
obj = MyModel(属性=值,属性=值)
obj.属性=值
obj.save()

from bookstore.models import Book
b2 = Book(title='Django',pub='清华大学出版社',price=70,market_price=80)
b2.save()
```

python manage.py shell启动django shell进行调试



#### ORM查询操作

通过MyModel.objects管理器方法调用查询方法

**1、all()方法**

​	等同于select * from table，返回值是QuerySet容器对象，容器内存数组

```python
from bookstore.models import Book
a1 = Book.objects.all()
for book in a1:
    print(book.title)
```

在models.py文件Book类中定义\__str__方法定义查询打印样式


```python
def __str__(self):  # 定义查询打印样式
    return '%s_%s_%s_%s' % (self.title, self.pub, self.price, self.market_price)
```

**values('列1','列2',...)**

​	等同于：select 列1，列2 from table，返回值QuerySet，容器内存字典

```python
a2 = Book.objects.values()
for book in a2:
    print(book['title'])
```

**values_list('列1','列2',...)**

​	等同于：select 列1，列2 from table，返回值QuerySet，容器内存元组

```python
a3 = Book.objects.values_list()
for book in a3:
    print(book[1])
```

**order_by()**

排序查询

```python
a4 = Book.objects.order_by('-price')  # 按price降序
```

**filter(条件)**

条件查询，有多个条件时为并列查询，相当于and

```python
a5 = Book.objects.filter(pub='清华大学出版社')
for book in a5:
    print('书名：',book.title)
```

**exclude(条件)**

查询不包含此条件的全部数据集

```python
a6 = Book.objects.exclude(pub='清华大学出版社')
for book in a6:
    print(book)
```

**get(条件)**

返回满足条件的唯一数据，只能返回一条数据，查询结果多余一条或为空都将抛出异常。



#### 查询谓词

**__exact等值匹配**

```python
Book.objects.filter(id__exact=1)
# 相当于select * from book where id =1
```

**__contains:包含指定值**

```python
Author.objects.filter(name__contains='w')
# 相当于 select * from author where name like '%w%'  模糊匹配
```

**__startswith：以xxx开始**（w%）

**__endswitsh：以xxx结束** （%w）

**__gt：大于指定值**

```python
Author.objects.filter(age_gt=50)
# 相当于select * from author where age>50
```

**__gte：大于等于指定值**

**__lt：小于指定值**

**__lte：小于等于指定值**

**__in：查询指定范围**

```python
Author.objects.filter(country__in=['中国'])
# 相当于select * from author where country in ('中国')
```

**__range：查询指定区间**

```python
Author.objects.filter(age_range=(35,50))
```



#### 更新数据

**更新单个数据**（get方法查询）

```python
b1 = Book.objects.get(id=2)
b1.pub='清华大学出版社'
b1.save()
```

**批量数据更新**

直接调用QuerySet的update（属性=值）实现批量修改

```python
books=Book.objects.filter(id__gt=3)
books.update(price=0)  # 将id大于3的图书价格定为0
```



#### 删除数据

**删除单个数据**

```python
try:
    auth = Author.objects.get(id=1)
    auth.delete()
except:
    print('删除失败')
```

**删除批量数据**

```python
auths = Author.objects.filter(age__get=65)
auths.delete()
```

伪删除（is_active）



#### F对象和Q对象

**F对象**

更新操作：Book实例中所有的零售价涨10元

```python
from django.db.models import F

Book.objects.all().update(market_price = F('market_price')+10)
```

对数据库中两个字段的值进行比较，列出哪些书的零售价高于定价

```python
from django.db.models import F
from bookstore.models import Book
books = Book.objects.filter(market_price__gt=F('price'))
for book in books:
    print(book.title, '定价：',book.price,'零售价：',book.market_price)
```

**Q对象**

当在获取查询结果集使用复杂的逻辑或|、逻辑非~等操作时可以借助Q对象

如：想找出定价低于20元或清华大学出版社的全部书：

```python
from django.db.models import Q

Book.objects.filter(Q(price__lt = 20)|Q(pub = '清华大学出版社'))
```

```python
from django.db.models import Q

Q(条件1)|Q(条件2)   # 或操作
Q(条件1)&Q(条件2)   # 与操作
Q(条件1)~Q(条件2)   # 非操作
```



#### admin配置

1、创建后台管理账号：

```python
python manage.py createsuperuser
```

2、注册自定义模型类

​	在应用app中的admin.py中导入注册要管理的模型model类

```python
from . models import Book
```

​	调用admin.site.register方法进行注册

```python
admin.site.register(自定义模型类)
```



**模型管理器类**

必须继承django.contrib.admin里的ModelAdmin类

1、在<应用app>/admin.py里定义模型管理器类

```python
class XXXManager(admin.ModelAdmin):
    ......
```

2、绑定注册模型管理器和模型类

```python
from django.contrib import admin
from .models import *
admin.site.register(YY,XXXManager)  # 绑定YY模型类与管理器类XXXManager
```

```python
from django.contrib import admin
from .models import Book

class BookManager(admin.ModelAdmin):
    # 列表页显示哪些字段的列
    list_display = ['id', 'title', 'pub', 'price', 'market_price']
    # 控制list_display中字段哪些可以链接到修改页,默认ID
    list_display_links = ['title']
    # 过滤器
    list_filter = ['pub']
    # 添加搜索框[模糊查询]
    search_fields = ['title']
    # 添加可在列表页编辑的字段
    list_editable = ['price']

admin.site.register(Book, BookManager)
```



#### 关系映射

一对一：OneToOneField（类名，on_delete=xxx）

```python
class A(model.Model):
    ...
class B(model.Model):
    属性 = models.OneToOneField(A,on_delete=xxx)
```

**on_delete级联删除**

1、models.CASCADE，删除包含ForeignKey的对象

2、models.PROTECT，阻止被引用的对象删除

3、SET_NULL，设置ForeignKey null，需要指定null=True

4、SET_DEFAULT ，将ForeignKey设置为其默认值，必须设置ForeignKey的默认值

```python
from django.db import models

class Author(models.Model):
    name = models.CharField('姓名', max_length=11)

class Wife(models.Model):
    name = models.CharField('姓名', max_length=11)
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
```

**创建数据**

无外键的模型类（Author）

```python
author1 = Author.objects.create(name='王老师')
```

有外键的模型类（Wife）

```python
wife1 = Wife.objects.create(name='王夫人', author=author1)
```

```python
wife1 = Wife.objects.create(name='王夫人', author_id=1)
```

**查询数据**

正向查询(有外键查无外键)

```python
# 通过wife找author
from .models import Wife
wife = Wife.objects.get(name='wnagfuren')
print(wife.author.name)
```

反向查询

```python
author1 = Author.objects.get(name='wang')
author1.wife.name
```

一对多：

```python
class A(models.Model):
    ...
class B(models.Model):  # 在多表上创建外键
    属性 = models.ForeignKey("一"的模型类, on_delete=xx)
```

```python
from django.db import models

class Publisher(models.Model):
    name = models.CharField('出版社名称', max_length=50)
    
class Book(models.Model):
    title = models.CharField('书名', max_length=11)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)  # 一对多

```

创建数据

```python
from .models import *
pub1 = Publisher.objects.create(name='清华大学出版社')
Book.objects.create(title='Python', publisher=pub1)
Book.objects.create(title='Java', publisher_id=pub1.id)
```

正向查询（通过Book查询Publisher）

```python
book.publisher.name
```

反向查询（通过Publisher查询对应的所有Book）

```python
# 通过出版社查询对应的书
pub1 = Publisher.objects.get(name='清华大学出版社')
books = pub1.book_set.all()  #通过book_set获取pub1对应的多个Book数据对象
# books = Book.objects.filter(publisher=pub1)
print('清华大学出版社的书有：')
for book in books:
    print(book.title)
```

多对多：

```python
属性 = models.ManyToManyField(MyModel)
```

```python
from django.db import models

class Author(models.Model):
    name = models.CharField('作者', max_length=20)
class Book(models.Model):
    title = models.CharField('书名', max_length=100)
    authors = models.ManyToManyField(Author)
```

创建数据

```python
# 方案1 先创建author再关联book
author1 = Author.objects.create(name='吕老师')
author2 = Author.objects.create(name='王老师')
# 吕老师和王老师共同写了一本Python
book1 = author1.book_set.all(title='Python')
author2.book_set.add(book1)

#方案2 先创建book再关联author
book = Book.objects.create(title='Django')
# Django由吕老师和张老师共同创作
author3 = book.authors.create(name='张老师')
book.authors.add(author1)
```

查询数据

正向查询(有属性authors的查)

```python
book.authors.all()
book.authors.filter(age__gt=80)
```

反向查询（通过Authors查询对应的所有Book）

```python
author.book_set.all()
author.book_set.filter()
```



#### cookies和session

```python
HttpResponse.set_cookie(key,value='',max_age=None,expires=None)
# key:cookie的名字
# value：cookie的值
# max_age：cookie存活时间，单位为秒
# expires：具体过期时间
```

**存储示例**

添加cookiess

```python
responds = HttpResponse('已添加my_varl,值为123')
responds.set_cookie('my_varl', 123, 3600)
return responds
```

修改cookies

```python
cookie
responds = HttpResponse('已修改my_varl,值为456')
responds.set_cookie('my_varl', 456, 3600*2)
return responds
```

删除cookiess

```python
HttpResponse.delete_cookie(key)  # 删除指定的key的cookie
```

获取cookies

​	通过request.COOKIES绑定的字典（dict）获取客户端的COOKIES数据

```python
value = request.COOKIES.get('cookies名', '默认值')
```



1、保存session的值到服务器

```python
request.session['KEY'] = VALUE
```

2、获取session的值

```python
value = request.session['KEY']
value = request.session.get('KEY', 默认值)
```

3、删除session

```python
del request.session['KEY']
```



### 云笔记项目

用户模块

​	1、注册 - 成为平台用户

​	2、登录 - 校验用户身份

​	3、退出登录 - 退出登录状态

笔记模块

​	1、查看笔记列表 ——查

​	2、创建新笔记——增

​	3、修改笔记——改

​	4、删除笔记——删





#### 缓存

数据库缓存（在settings.py中配置）

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        'TIMEOUT': 300,  # 缓存保存时间 单位秒，默认值为300
        'OPTIONS': {
            'MAX_ENTRIES': 300,  # 缓存最大数据条数
            'CULL_FREQUENCY': 2,  # 缓存条数达到最大值时，删除1/x的缓存数据
        }
    }
}

```

需要手动创建数据库（my_cache_table）

```python
python manage.py createcachetable  # 在终端中执行创建数据库
```

**整体缓存策略**

Django中使用缓存

在视图函数中

```python
from django.views.decorators.cache import cache_page

@cache_page(30)
def my_view(request):
    ...
```

在路由中

```python
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('foo/', cache_page(60)(my_view)),
]
```

**局部缓存策略**

先引入cache对象

​	方式1：

```pyhton
from django.core.cache import caches

cache1 = caches['myalias']
cache2 = caches['myalias_2']
```

​	方式2：

```python
from django.core.cache import cache # 相当于直接引入CACHES配置项中的'default'项
```

1、cache.set(key, value, timeout)   - 存储缓存

2、cache.get(key)  - 获取缓存

3、cache.add(key,value)  -存储缓存，只在key不存在时生效

4、cache.get_or_set(key,value,timeout)  -如果未获取到数据则执行set操作

5、cache.set_many(dict,timeout)  -批量存储缓存

6、cache.get_many(key_list)  -批量获取缓存数据





#### 分页

**Paginator**负责分页数据整体的管理

对象的构造方法

```python
paginator = Paginator(object_list, per_page)
# object_list 需要分页数据的对象列表
# per_page 每页数据的个数
# 返回值Paginator的对象
```

Paginator属性

- count：需要分页数据的对象总数
- num_pages：分页后的页面总数
- page_range：从1开始的range对象，用于记录当前页码数
- per_page：每页数据的个数

Paginator方法

- paginator对象.page(number)

  **Page对象**

  创建对象

  ```python
  page = paginator.page(页码)
  ```

  Page对象属性

  - object_list：当前页上所有数据对象的列表

  - number：当前页的序号，从1开始

  - paginator：当前page对象相关的Paginator对象

  Page对象的方法
  
  - has_next()
  - has_previous()
  - has_other_pages()
  - next_page_number()：返回下一页的页码
  - previous_page_number()：返回上一页的页码
  

```python
def test_page(request):
    # 利用查询字符串 /test_page?page=1
    page_num = request.GET.get('page', 1)
    all_data = ['a', 'b', 'c', 'd', 'e']
    paginator = Paginator(all_data, 2)  # 初始化paginator
    # 初始化具体页码的page对象
    c_page = paginator.page(int(page_num))
    return render(request, 'test_page.html', locals())
```





python中生成csv文件

```python
import csv

with open('eggs.csv', 'w', newline='') as csvfile:
    write = csv.writer(csvfile)
    write.writerow(['a', 'b', 'c'])
```

实现csv文件下载

- 响应Conten-Type类型需修改为text/csv

- 响应会获得一个额外的Content-Disposition标头，其中包含csv文件的名称

```python
from django.http import HttpResponse
from .models import Book
import csv

def test_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="text.csv"'
    all_book = Book.objects.all()
    writer = csv.writer(response)
    writer.writerow(['id', 'title'])
    for b in all_book:
        writer.writerow([b.id, b.title])
    return response
```



#### 内建用户系统

```python
from django.contrib.auth.models import User
```

**创建用户**

创建普通用户create_user

```python
from django.contrib.auth.models import User

user = User.objects.create_user(username='用户名',password='密码',email='',...)
```

创建超级用户create_superuser

```python
from django.contrib.auth.models import User

user = User.objects.create_superuser(username='用户名',password='密码',email='',...)
```

校验密码

```python
from django.contrib.auth import authenticate

user = authenticate(username=username,password=password)
```

修改密码

```python
from django.contrib.auth.models import User

try:
    user = User.objects.get(user='用户名')
    user.set_password('654321')
    user.save()
    return HttpResponse('修改密码成功')
except:
    return HttpResponse('修改密码失败')
```

登录状态保持

```python
from django.contrib.auth import login

def login_view(request):
    user = authenticate(username=username,password=password)
    login(request,user)
```

登录状态校验

```python
from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
    # 该视图必须为用户登录状态下才可访问
    # 当前登录用户可通过request.user直接获取
    login_user = request.user
    ...
```

登录状态取消

```python
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
```

内建用户表-扩展字段

方案1：通过建立新表，跟内建表做1对1

方案2：继承内建的抽象user模型类

- 添加应用

- 定义模型类，继承AbstractUser

- settings.py中指明AUTH_USER_MODEL=‘应用名.类名’



#### 文件上传

在settings.py文件中设置MEDIA相关配置

```python
# file : settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

MEDIA_URL和MEDIA_ROOT需要手动绑定

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

文件写入

**open方式**

```python
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
```

**借助ORM**

模型类的字段：FileField()

```python
from django.db import models

class Content(models.Model):
    title = models.CharField('标题', max_length=100)
    picture = models.FileField(upload_to='picture')
```



#### 发送邮件

配置文件

```python
# qq邮箱授权码：xrolqfpjwwbsebhe
# 邮件相关配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # 腾讯qq邮箱SMTP服务器地址
EMAIL_PORT = 25
EMAIL_HOST_USER = '2376935197@qq.com'
EMAIL_HOST_PASSWORD = 'xrolqfpjwwbsebhe'  # 邮箱授权码
```

函数调用

```python
from django.core import mail

mail.send_mail(subject,  # 主题
               message,  # 内容
               from_email,  # 发送者[当前配置邮箱]
               recipient_list=['xxx@qq.com'],  # 接收者邮件列表
              )
```

利用中间件捕获异常发送邮件

