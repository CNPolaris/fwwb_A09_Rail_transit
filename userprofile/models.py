from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


# Create your models here.
# 用户拓展信息
class Profile(models.Model):
    # 与User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 用户roles
    roles = models.CharField(max_length=10, blank=True, null=True)
    # 是否在线 1是0否
    online = models.IntegerField(blank=True, null=True)
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True, null=True)
    # 头像
    avatar = models.CharField(max_length=150, blank=True, null=True)
    # 个人简介
    introduction = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


@receiver(pre_delete, sender=User)
def user_delete(sender, instance,**kwargs):
    Profile.objects.get(user=instance).delete()


# 信号接收函数，每当新建User实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收函数，每当更新user实例化时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Permission(models.Model):
    permission = models.CharField(max_length=10,verbose_name="权限等级", null=True)
    rule = models.CharField(max_length=20, verbose_name="权限规则", null=True)
    description = models.CharField(max_length=30, verbose_name="描述", null=True)