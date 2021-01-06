from django.db import models


# Create your models here.
# 节日的model
class Workdays(models.Model):
    # 日期
    date = models.DateTimeField()
    # 节日
    festival = models.CharField(max_length=255, blank=True)

    # 按照日期进行降序排列
    class Meta:
        ordering = ['-date']


# 站点的model
class Station(models.Model):
    # 站点编号
    Station_id = models.IntegerField()
    # 站点名称
    Station_name = models.CharField(max_length=255)
    # 路线
    Station_route = models.CharField(max_length=100)
    # 行政区域
    Admin = models.CharField(max_length=100)


# 乘车记录的model
class Trips(models.Model):
    # 乘客编号
    User_id = models.CharField(max_length=255)
    # 进站名
    In_name = models.CharField(max_length=100)
    # 进站时间
    In_time = models.DateTimeField()
    # 出站名
    Out_name = models.CharField(max_length=100)
    # 出站时间
    Out_time = models.DateTimeField()
    # 购票渠道
    Channel_id = models.IntegerField()
    # 票价
    Price = models.FloatField()


# 用户的model
class Users(models.Model):
    # 用户编号
    User_id = models.CharField(max_length=255)
    # 区域
    Dist = models.IntegerField()
    # 出生日期
    Birth = models.IntegerField()
    # 性别
    Gender = models.IntegerField()
