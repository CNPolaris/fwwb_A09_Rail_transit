import django
from django.db.models import Count
from django.shortcuts import render
# 导入 HttpResponse 模块
from django.http import HttpResponse, JsonResponse
import time
# 导入行程model
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.core.cache import cache, utils
from .models import Trips, Users, Workdays, Station, TripStatistics, Menu
# 导入表单类
from .forms import TripsForm
# 引入redirect重定向模块
from django.shortcuts import render, redirect
import datetime
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from transit.mixins import BaseRequiredMixin, get_user_config
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeDoneView,
    PasswordChangeView
)

login = LoginView.as_view(template_name='accounts/login.html')

logout = LogoutView.as_view(template_name='accounts/logout.html')

password_reset = PasswordResetView.as_view(
    template_name='accounts/password_reset_form.html',
    email_template_name='accounts/password_reset_email.html',
    subject_template_name='accounts/password_reset_subject.txt',
)

password_reset_done = PasswordResetDoneView.as_view(
    template_name='accounts/password_reset_done.html'
)

reset = PasswordResetConfirmView.as_view(
    template_name='accounts/password_reset_confirm.html'
)

reset_done = PasswordResetCompleteView.as_view(
    template_name='accounts/password_reset_complete.html'
)


class PasswordChangeView(BaseRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('transit:index')


password_change = PasswordChangeView.as_view()

password_change_done = PasswordChangeDoneView.as_view(
    template_name='accounts/password_change_done.html'
)


# Create your views here.
# 首页视图
class IndexView(BaseRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['date'] = datetime.date.today().strftime("%Y-%m-%d")
        return context
