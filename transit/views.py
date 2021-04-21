from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from transit.models import Users
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from rest_framework_jwt.serializers import jwt_decode_handler
from transit.serializers import PassengerSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = PassengerSerializer
    page = PageNumberPagination()
    page.page_size = 20
    params_dict = {}
    sort = None

    def get_permissions(self):
        """
        验证权限
        :return:
        """
        if self.request.method == 'GET' or 'PUT':
            self.permission_classes = [AllowAny]
        # else:
        #     self.permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]

        return super().get_permissions()

    def get_query_params(self):
        """
        解析请求参数
        :return: dict
        """
        uid = self.request.query_params.get('passenger_id', None)
        if uid:
            self.params_dict['user_id'] = uid
        dist = self.request.query_params.get('dist', None)
        if dist:
            self.params_dict['dist'] = dist
        birth = self.request.query_params.get('birth', None)
        if birth:
            self.params_dict['birth'] = birth
        gender = self.request.query_params.get('gender', None)
        if gender:
            self.params_dict['gender'] = gender

        self.sort = self.request.query_params.get('sort', None)
        self.page.page_size = self.request.query_params.get('limit', 20)
        self.page.page = self.request.query_params.get('page', 1)

    def get_request_data(self):
        """
        提取消息体数据
        :return: dict
        """
        data = {}
        uid = self.request.data.get('passenger_id', None)
        if uid:
            data['user_id'] = uid
        dist = self.request.data.get('dist', None)
        if dist is not None and isinstance(dist, int):
            data['dist'] = dist
        birth = self.request.data.get('birth', None)
        if birth is not None and isinstance(birth, int):
            data['birth'] = birth
        gender = self.request.data.get('gender', None)
        if gender is not None and gender in [0, 1]:
            data['gender'] = gender
        return data

    def valid_create_data(self, form):
        """
        用来代替不能使用表单类的情况下数据的验证器
        :return: Bool
        """
        if form['user_id'] is None:
            return False
        if form['birth'] is None or not isinstance(form['birth'], int):
            return False
        if form['gender'] is None or not form['gender'] in [0, 1]:
            return False
        if form['dist'] is None or not isinstance(form['dist'], int):
            return False
        return True

    def get_queryset(self):
        """
        过滤数据集
        :return: querySet
        """
        self.get_query_params()
        queryset = self.queryset
        return queryset.filter(**self.params_dict)

    def list(self, request, *args, **kwargs):
        """
        列出所有的passenger信息
        :param request: GET /api/manage/pass
        :param args:
        :param kwargs:
        :return: json
        """
        queryset = self.get_queryset()
        if queryset:
            ret_page = self.page.paginate_queryset(queryset, request, self)
            passenger_serializer = self.serializer_class(ret_page, many=True)
            context = {
                'code': 2000,
                'total': queryset.count(),
                'data': passenger_serializer.data
            }
            return Response(context)
        else:
            context = {
                'code': 1000,
                'total': queryset.count(),
                'data': [],
                'message': '查询结果为空'
            }
            return Response(context)

    def create(self, request, *args, **kwargs):
        """
        创建数据
        :param request: POST /api/manage/pass
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        form = self.get_request_data()
        if self.valid_create_data(form):
            try:
                new_user = Users(**form)
                new_user.save()
                context['code'] = 2000
                context['message'] = '创建数据成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '创建失败,出现错误{}'.format(e)
        return Response(context)

    def update(self, request, *args, **kwargs):
        """
        更新数据
        :param request: PUT /api/manage/pass
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        queryset = self.get_queryset()
        if queryset:
            form = self.get_request_data()
            queryset.update(**form)
            context['code'] = 2000
            context['message'] = '数据更新成功'
            context['data'] = list(queryset.values())
        else:
            context['code'] = 1000
            context['message'] = '查询结果为空'
        return Response(context)

    def destroy(self, request, *args, **kwargs):
        """
        删除数据
        :param request: DELETE /api/manage/pass
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        uid = self.request.query_params.get('passenger_id', None)
        try:
            passenger = Users.objects.get(user_id=uid)
            passenger.delete()
            context['code'] = 2000
            context['message'] = '删除成功'
        except BaseException as e:
            context['code'] = 1000
            context['message'] = '数据删除失败, {}'.format(e)
        return Response(context)
