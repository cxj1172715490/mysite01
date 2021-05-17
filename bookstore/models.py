from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField('书名', max_length=50, default='', unique=True)
    pub = models.CharField('出版社', max_length=100, default='')
    price = models.DecimalField('价格', max_digits=7, decimal_places=2)
    market_price = models.DecimalField('零售价', max_digits=7, decimal_places=2, default=0.0)
    is_active = models.BooleanField('是否活跃', default=True)  # 新增字段必须具备默认值

    class Meta:  # 修改数据表名称
        db_table = 'book'
        verbose_name = '图书'  # 修改在admin中的名称显示
        verbose_name_plural = '图书'

    def __str__(self):  # 定义查询打印样式
        return '%s_%s_%s_%s_%s' % (self.id, self.title, self.pub, self.price, self.market_price)


class Author(models.Model):
    name = models.CharField('姓名', max_length=11)
    age = models.IntegerField('年龄', default=1)
    email = models.EmailField('邮箱', null=True)

    class Meta:
        db_table = 'author'
