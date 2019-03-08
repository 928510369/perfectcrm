from django.db import models

# Create your models here.
class Author(models.Model):

    name=models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=64,verbose_name="书名")
    color = models.CharField(max_length=64)
    price=models.CharField(max_length=64,error_messages={},validators=())
    page_num=models.IntegerField()
    author=models.ForeignKey(Author)
    def __str__(self):
        return self.title
class User(models.Model):
    name=models.CharField(max_length=64)
    email=models.EmailField(null=True,default=" ")
    infi=models.ForeignKey(to="Userdetiel",to_field="id",)
    m2m=models.ManyToManyField(to="Mf")
    def clean(self):
        print(self.name)
        pass
    def __str__(self):
        return self.name
class Userdetiel(models.Model):
    info=models.CharField(max_length=64)
    def __str__(self):
        return self.info
class Mf(models.Model):
    content=models.CharField(max_length=64,null=True,default=" ")

class Level(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Direction(models.Model):
    name = models.CharField(max_length=32)
    d_2_c = models.ManyToManyField('Category')

class Category(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Video(models.Model):
    lv = models.ForeignKey(Level)
    cg = models.ForeignKey(Category)

    title = models.CharField(verbose_name='标题', max_length=32)
    summary = models.CharField(verbose_name='简介', max_length=32)
    img = models.ImageField(verbose_name='图片', upload_to='./static/images/Video/')
    href = models.CharField(verbose_name='视频地址', max_length=256)

    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title