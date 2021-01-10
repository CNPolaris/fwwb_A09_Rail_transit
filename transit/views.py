import django
from django.db.models import Count
from django.shortcuts import render
# 导入 HttpResponse 模块
from django.http import HttpResponse, JsonResponse
import time
# 导入行程model
from .models import Trips, Users, Workdays, Station, TripStatistics
# 导入表单类
from .forms import TripsForm
# 引入redirect重定向模块
from django.shortcuts import render, redirect
import datetime
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.db.models import Q


# Create your views here.
# 首页展示图谱视图
def index(request):
    return render(request, 'index.html')


