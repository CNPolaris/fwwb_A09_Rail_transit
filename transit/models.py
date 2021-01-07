from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone


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


# 每日客流量实时统计
class TripStatistics(models.Model):
    # 日期
    date = models.DateField(timezone.now().strftime("%Y-%m-%d"), primary_key=True)
    # 实时出行统计
    count = models.IntegerField()

    class Meta:
        ordering = ["-date"]


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


@receiver(post_save, sender=Trips)
def countAdd(instance, **kwargs):
    """
    当Trips新增一条数据之后，会调用countAdd函数对TripStatistics对应的日期下的count进行自加
    :param instance: Trips 新增数据保存后 instance是被修改的实例
    :param kwargs:
    :return: null
    """
    try:
        search = TripStatistics.objects.get(date=instance.In_time.strftime("%Y-%m-%d"))
        print("查询结果存在")
        search.count = search.count + 1
        search.save()
        print("客流量记录增加完成")
    except:
        print("查询结果不存在，需要添加")
        search = TripStatistics(instance.In_time.strftime("%Y-%m-%d"), 0)
        search.count = search.count + 1
        search.save()
        print("客流量记录增加完成")


@receiver(post_delete, sender=Trips)
def countReduce(instance, **kwargs):
    """
    当Trips删除一条记录时，对应当天的客流量也会随之减少
    :param instance: 被删除的实例
    :param kwargs:
    :return: null
    """
    search = TripStatistics.objects.get(date__contains=instance.In_time.strftime("%Y-%m-%d"))
    search.count = search.count - 1
    search.save()
    print("客流量记录减少完成")
