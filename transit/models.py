from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone


# Create your models here.
# 用户的model
class Users(models.Model):
    # 用户编号
    user_id = models.CharField(primary_key=True, max_length=255, verbose_name="用户编号")
    # 区域
    dist = models.IntegerField(verbose_name="区域")
    # 出生日期
    birth = models.IntegerField(verbose_name="出生日期")
    # 性别
    gender = models.IntegerField(verbose_name="性别")


# 站点的model
class Station(models.Model):
    # 站点编号
    station_id = models.IntegerField(primary_key=True, verbose_name="站点编号")
    # 站点名称
    station_name = models.CharField(max_length=255, verbose_name="站点名称")
    # 路线
    station_route = models.CharField(max_length=100, verbose_name="行驶路线")
    # 行政区域
    admin_area = models.CharField(max_length=100, verbose_name="行政区域")


# 乘车记录的model
class Trips(models.Model):
    # 乘客编号
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="乘客编号")
    # 进站名
    in_station = models.CharField(max_length=255, verbose_name="入站点")
    # 进站时间
    in_station_time = models.DateTimeField(verbose_name="进站时间")
    # 出站名
    out_station = models.CharField(max_length=255, verbose_name="出站点")
    # 出站时间
    out_station_time = models.DateTimeField(verbose_name="出站时间")
    # 购票渠道
    channel = models.IntegerField(verbose_name="购票渠道")
    # 票价
    price = models.FloatField(verbose_name="票价")


# 每日客流量实时统计
class TripStatistics(models.Model):
    # 日期
    date = models.DateField(primary_key=True, verbose_name="日期")
    # 实时出行统计
    count = models.IntegerField(verbose_name="客流统计")

    class Meta:
        ordering = ["-date"]


# 节日的model
class Workdays(models.Model):
    # 日期
    date = models.DateField(primary_key=True, verbose_name="日期")
    # 节日
    date_class = models.CharField(max_length=255, blank=True, verbose_name="日期属性")

    # 按照日期进行降序排列
    class Meta:
        ordering = ['-date']


# list model
class Menu(models.Model):
    model_name = models.CharField(max_length=50, verbose_name="模块名称")
    model_verbose = models.CharField(max_length=50, verbose_name="模块说明")
    icon = models.CharField(max_length=20, verbose_name="图标")
    icon_color = models.CharField(max_length=50, verbose_name="图标颜色")


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
