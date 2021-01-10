import django
from django.db.models import Count
from django.shortcuts import render
# 导入 HttpResponse 模块
from django.http import HttpResponse, JsonResponse
import time
# 导入行程model
from .models import Trips, Users, Workdays, Station, TripStatistics, Menu
# 导入表单类
from .forms import TripsForm
# 引入redirect重定向模块
from django.shortcuts import render, redirect
import datetime
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.db.models import Q
from django.views.generic import TemplateView


# Create your views here.
# 首页视图
class IndexView(TemplateView):
    template_name = 'index.html'

    def make_menu(self):
        Menu_list = Menu.objects.all()
        menus = [
            {
                'model_name': menu.model_name,
                'verbose': menu.model_verbose,
                'icon': menu.icon,
                'icon_color': menu.icon_color
            } for menu in Menu_list
        ]
        return menus

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['menus'] = self.make_menu()
        return context
