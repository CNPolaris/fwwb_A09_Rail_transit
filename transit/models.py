from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone


# Create your models here.
# 用户的model
class Users(models.Model):
    # 用户编号
    user_id = models.CharField(primary_key=True, max_length=255)
    # 区域
    dist = models.IntegerField()
    # 出生日期
    birth = models.IntegerField()
    # 性别
    gender = models.IntegerField()


# 站点的model
class Station(models.Model):
    # 站点编号
    station_id = models.IntegerField(primary_key=True)
    # 站点名称
    station_name = models.CharField(max_length=255)
    # 路线
    station_route = models.CharField(max_length=100)
    # 行政区域
    admin_area = models.CharField(max_length=100)


# 乘车记录的model
class Trips(models.Model):
    # 乘客编号
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    # 进站名
    in_station = models.CharField(max_length=255)
    # 进站时间
    in_station_time = models.DateTimeField()
    # 出站名
    out_station = models.CharField(max_length=255)
    # 出站时间
    out_station_time = models.DateTimeField()
    # 购票渠道
    channel = models.IntegerField()
    # 票价
    price = models.FloatField()


# 每日客流量实时统计
class TripStatistics(models.Model):
    # 日期
    date = models.DateField(timezone.now().strftime("%Y-%m-%d"), primary_key=True)
    # 实时出行统计
    count = models.IntegerField()

    class Meta:
        ordering = ["-date"]


# 节日的model
class Workdays(models.Model):
    # 日期
    date = models.DateField(primary_key=True)
    # 节日
    date_class = models.CharField(max_length=255, blank=True)

    # 按照日期进行降序排列
    class Meta:
        ordering = ['-date']


# list model
class Menu(models.Model):
    model_name = models.CharField(max_length=50, verbose_name="模块名称")
    model_verbose = models.CharField(max_length=50)
    icon = models.CharField(max_length=20)
    icon_color = models.CharField(max_length=50)


@receiver(post_save, sender=Trips)
def countAdd(instance, **kwargs):
    """
    当Trips新增一条数据之后，会调用countAdd函数对TripStatistics对应的日期下的count进行自加
    :param instance: Trips 新增数据保存后 instance是被修改的实例
    :param kwargs:
    :return: null
    """
    try:
        search = TripStatistics.objects.get(date=instance.in_station_time.strftime("%Y-%m-%d"))
        print("查询结果存在")
        search.count = search.count + 1
        search.save()
        print("客流量记录增加完成")
    except:
        print("查询结果不存在，需要添加")
        search = TripStatistics(instance.in_station_time.strftime("%Y-%m-%d"), 0)
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
    search = TripStatistics.objects.get(date__contains=instance.in_station_time.strftime("%Y-%m-%d"))
    search.count = search.count - 1
    search.save()
    print("客流量记录减少完成")
