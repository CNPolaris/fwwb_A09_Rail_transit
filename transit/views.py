from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from transit.models import Users, Workdays, Trips, Station
from transit.serializers import PassengerSerializer, WorkdaySerializer, StationSerializer, TripSerializer
from userprofile.permissions import IsSelfOrReadOnly, IsAdminUserOrReadOnly


# 自定义分页类
class MyPageNumberPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 20
    # 默认每页显示3个，可以通过传入pager1/?page=2&limit=4,改变默认每页显示的个数
    page_size_query_param = "limit"
    # # 最大页数不超过10
    # max_page_size = 10
    # 获取页码数的
    page_query_param = "page"


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = PassengerSerializer
    pagination = MyPageNumberPagination()
    params_dict = {}
    sort = None

    def get_permissions(self):
        """
        验证权限
        :return:
        """
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUserOrReadOnly]

        return super().get_permissions()

    def get_query_params(self):
        """
        解析请求参数
        :return: dict
        """
        self.params_dict = self.request.query_params.dict()
        if 'token' in self.params_dict.keys():
            del self.params_dict['token']
        if 'page' in self.params_dict.keys():
            del self.params_dict['page']
        if 'limit' in self.params_dict.keys():
            del self.params_dict['limit']
        if 'sort' in self.params_dict.keys():
            del self.params_dict['sort']

        self.sort = self.request.query_params.get('sort', None)

    def get_request_data(self):
        """
        提取消息体数据
        :return: dict
        """
        data = {}
        uid = self.request.data.get('user_id', None)
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

    def valid_users_data(self, form):
        """
        用来代替不能使用表单类的情况下数据的验证器
        :return: Bool
        """
        if form['user_id'] is None:
            return False, 'user_id'
        if form['birth'] is None or not isinstance(form['birth'], int):
            return False, 'birth'
        if form['gender'] is None or not form['gender'] in [0, 1]:
            return False, 'gender'
        if form['dist'] is None or not isinstance(form['dist'], int):
            return False, 'dist'
        return True, ''

    def get_queryset(self):
        """
        过滤数据集
        :return: querySet
        """
        self.get_query_params()
        if self.params_dict:
            if self.sort:
                queryset = self.queryset.filter(**self.params_dict).order_by(self.sort)
            else:
                queryset = self.queryset.filter(**self.params_dict)
        else:
            queryset = self.queryset
        return queryset

    def list(self, request, *args, **kwargs):
        """
        列出所有的passenger信息
        :param request: GET /api/manage/passenger
        :param args:
        :param kwargs:
        :return: json
        """
        queryset = self.get_queryset()
        if queryset.exists():
            ret_page = self.pagination.paginate_queryset(queryset, request, self)
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
        创建passenger数据
        :param request: POST /api/manage/passenger
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        form = self.get_request_data()
        flag, msg = self.valid_users_data(form)
        if flag:
            try:
                new_user = Users(**form)
                new_user.save()
                context['code'] = 2000
                context['message'] = '创建数据成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '创建失败,出现错误{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '数据不符合规范,{}'.format(msg)
        return Response(context)

    def update(self, request, *args, **kwargs):
        """
        更新passenger数据
        :param request: PUT /api/manage/passenger
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        uid = self.request.data.get('user_id', None)
        queryset = self.get_queryset().filter(user_id=uid)
        if queryset.exists():
            form = self.get_request_data()
            flag, msg = self.valid_users_data(form)
            if flag:
                try:
                    queryset.update(**form)
                    context['code'] = 2000
                    context['message'] = '数据更新成功'
                    context['data'] = list(queryset.values())
                except BaseException as e:
                    context['code'] = 2000
                    context['message'] = '数据更新失败,{}'.format(e)
            else:
                context['code'] = 1000
                context['message'] = '数据不符合规范,{}'.format(msg)
        else:
            context['code'] = 1000
            context['message'] = '不存在指定数据'
        return Response(context)

    def destroy(self, request, *args, **kwargs):
        """
        删除passenger数据
        :param request: DELETE /api/manage/passenger
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        uid = self.request.data.get('passenger_id', None)
        try:
            passenger = Users.objects.get(user_id=uid)
            passenger.delete()
            context['code'] = 2000
            context['message'] = '删除成功'
        except BaseException as e:
            context['code'] = 1000
            context['message'] = '数据删除失败, {}'.format(e)
        return Response(context)


class WorkdayViewSet(viewsets.ModelViewSet):
    queryset = Workdays.objects.all()
    serializer_class = WorkdaySerializer
    page = MyPageNumberPagination()
    params_dict = {}
    sort = None

    def get_permissions(self):
        """
        验证权限
        :return:
        """
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUserOrReadOnly]
        return super().get_permissions()

    def get_query_params(self):
        """
        解析请求参数
        :return: dict
        """
        self.params_dict = {}
        date = self.request.query_params.get('date', None)
        if date:
            self.params_dict['date'] = date
        cls = self.request.query_params.get('date_class', None)
        if cls:
            self.params_dict['date_class'] = cls

        self.sort = self.request.query_params.get('sort', None)

    def get_request_data(self):
        """
        提取消息体数据
        :return: dict
        """
        data = {}
        date = self.request.data.get('date', None)
        if date:
            data['date'] = date
        cls = self.request.data.get('date_class', None)
        if cls:
            data['date_class'] = cls
        return data

    def valid_workday_data(self, form):
        """
        用来代替不能使用表单类的情况下数据的验证器
        :return: Bool
        """
        for key in ['date', 'date_class']:
            try:
                if form[key] is None:
                    return False
            except BaseException as e:
                return False
        return True

    def get_queryset(self):
        """
        过滤数据集
        :return: querySet
        """
        self.get_query_params()
        if self.params_dict:
            queryset = self.queryset.filter(**self.params_dict)
        else:
            queryset = self.queryset.filter()
        if self.sort:
            queryset = queryset.order_by(self.sort)
        return queryset

    @csrf_exempt
    def list(self, request, *args, **kwargs):
        """
        列出所有的Workday信息
        :param request: GET /api/manage/workday
        :param args:
        :param kwargs:
        :return: json
        """
        queryset = self.get_queryset()
        if queryset.exists():
            ret_page = self.page.paginate_queryset(queryset, request, self)
            passenger_serializer = self.serializer_class(ret_page, many=True)
            context = {
                'code': 2000,
                'message': '获取数据成功',
                'total': queryset.count(),
                'data': passenger_serializer.data
            }
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
        创建Workday数据
        :param request: POST /api/manage/workday
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        form = self.get_request_data()
        if self.valid_workday_data(form):
            try:
                new_workday = Workdays(**form)
                new_workday.save()
                context['code'] = 2000
                context['message'] = '创建数据成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '创建数据失败, 出现错误{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '数据不符合规范'
        return Response(context)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        """
        更新Workday数据
        :param request: PUT /api/manage/workday
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        queryset = self.get_queryset()
        if queryset.exists():
            form = self.get_request_data()
            # TODO: 数据格式验证
            try:
                queryset.update(**form)
                context['code'] = 2000
                context['message'] = '数据更新成功'
                context['data'] = list(queryset.values())
            except BaseException as e:
                context['code'] = 2000
                context['message'] = '数据更新失败,{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '不存在指定数据'
        return Response(context)

    def destroy(self, request, *args, **kwargs):
        """
        删除Workday数据
        :param request: DELETE /api/manage/workday
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        date = self.request.data.get('date', None)
        if date:
            try:
                workday = Workdays.objects.get(date=date)
                workday.delete()
                context['code'] = 2000
                context['message'] = '删除失败'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '删除失败，{}'.format(e)
        return Response(context)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trips.objects.all()
    serializer_class = TripSerializer
    pagination = MyPageNumberPagination()
    params_dict = {}
    sort = None

    def get_permissions(self):
        """
        验证权限
        :return:
        """
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUserOrReadOnly]
        return super().get_permissions()

    def get_query_params(self):
        """
        解析请求参数
        :return: dict
        """
        self.params_dict = self.request.query_params.dict()
        if 'token' in self.params_dict.keys():
            del self.params_dict['token']
        if 'page' in self.params_dict.keys():
            del self.params_dict['page']
        if 'limit' in self.params_dict.keys():
            del self.params_dict['limit']
        if 'sort' in self.params_dict.keys():
            del self.params_dict['sort']
        self.sort = self.request.query_params.get('sort', 'id')

    def get_request_data(self):
        """
        提取消息体数据
        :return: dict
        """
        data = {}
        user_id = self.request.data.get('user_id')
        in_station = self.request.data.get('in_station', None)
        in_station_time = self.request.data.get('in_station_time', None)
        out_station = self.request.data.get('out_station', None)
        out_station_time = self.request.data.get('out_station_time', None)
        price = self.request.data.get('price', None)
        channel = self.request.data.get('channel', None)
        if user_id:
            data['user_id'] = user_id
        if in_station:
            data['in_station'] = in_station
        if in_station_time:
            data['in_station_time'] = in_station_time
        if out_station:
            data['out_station'] = out_station
        if out_station_time:
            data['out_station_time'] = out_station_time
        if price:
            data['price'] = price
        if channel:
            data['channel'] = channel
        return data

    def valid_trip_data(self, form):
        """
        用来代替不能使用表单类的情况下数据的验证器
        :return: Bool
        """
        if form['user_id'] is None:
            return False, form['user_id']
        if form['in_station'] is None or not Station.objects.get(station_name=form['in_station']):
            return False, form['in_station']
        if form['in_station_time'] is None:
            return False, form['in_station_time']
        if form['out_station'] is None or Station.objects.get(station_name=form['out_station']):
            return False, form['out_station']
        if form['out_station_time'] is None:
            return False, form['out_station_time']
        if form['channel'] is None or not isinstance(form['channel'], int):
            return False, form['channel']
        if form['price'] is None or not isinstance(form['price'], int):
            return False, form['price']
        return True, ''

    def get_queryset(self):
        """
        过滤数据集
        :return: querySet
        """
        self.get_query_params()
        if self.params_dict:
            queryset = self.queryset.filter(**self.params_dict)
        else:
            queryset = self.queryset.filter()
        if self.sort:
            queryset = queryset.order_by(self.sort)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        列出所有的Trip信息
        :param request: GET /api/manage/trip
        :param args:
        :param kwargs:
        :return: json
        """
        queryset = self.get_queryset()
        if queryset.exists():
            ret_page = self.pagination.paginate_queryset(queryset, request, self)
            passenger_serializer = self.serializer_class(ret_page, many=True)
            context = {
                'code': 2000,
                'message': '获取数据成功',
                'total': queryset.count(),
                'data': passenger_serializer.data
            }
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
        创建Trip数据
        :param request: POST /api/manage/trip
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        form = self.get_request_data()
        flag, msg = self.valid_trip_data(form)
        if flag:
            try:
                new_trip = Trips(**form)
                new_trip.save()
                context['code'] = 2000
                context['message'] = '创建数据成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '创建数据失败, 出现错误{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '数据不符合规范,{}'.format(msg)
        return Response(context)

    def update(self, request, *args, **kwargs):
        """
        更新Trip数据
        :param request: PUT /api/manage/trip
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        tid = self.request.data.get('id', None)
        queryset = self.get_queryset().filter(id=tid)
        if queryset.exists():
            form = self.get_request_data()
            # TODO: 数据格式验证
            try:
                queryset.update(**form)
                context['code'] = 2000
                context['message'] = '数据更新成功'
                context['data'] = list(queryset.values())
            except BaseException as e:
                context['code'] = 2000
                context['message'] = '数据更新失败,{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '不存在指定数据'
        return Response(context)

    def destroy(self, request, *args, **kwargs):
        """
        删除Trip数据
        :param request: DELETE /api/manage/trip
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        tid = self.request.data.get('id', None)
        if tid:
            try:
                trip = Trips.objects.get(id=tid)
                trip.delete()
                context['code'] = 2000
                context['message'] = '删除成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '删除失败，{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '删除失败'
        return Response(context)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    pagination = MyPageNumberPagination()
    params_dict = {}
    sort = None

    def get_permissions(self):
        """
        验证权限
        :return:
        """
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUserOrReadOnly]

        return super().get_permissions()

    def get_query_params(self):
        """
        解析请求参数
        :return: dict
        """
        self.params_dict = self.request.query_params.dict()
        if 'token' in self.params_dict.keys():
            del self.params_dict['token']
        if 'page' in self.params_dict.keys():
            del self.params_dict['page']
        if 'limit' in self.params_dict.keys():
            del self.params_dict['limit']
        if 'sort' in self.params_dict.keys():
            del self.params_dict['sort']
        self.sort = self.request.query_params.get('sort', None)

    def get_request_data(self):
        """
        提取消息体数据
        :return: dict
        """
        data = {}

        station_id = self.request.data.get('station_id', None)
        station_name = self.request.data.get('station_name', None)
        station_route = self.request.data.get('station_route', None)
        admin_area = self.request.data.get('admin_area', None)

        if station_id:
            data['station_id'] = station_id
        if station_name:
            data['station_name'] = station_name
        if station_route:
            data['station_route'] = station_route
        if admin_area:
            data['admin_area'] = admin_area
        return data

    def valid_station_data(self, form):
        """
        用来代替不能使用表单类的情况下数据的验证器
        :return: Bool
        """
        for key in ["station_id", "station_name", "station_route", "admin_area"]:
            try:
                if form[key] is None:
                    return False
                else:
                    continue
            except BaseException as e:
                print(e)
                return False
        return True

    def get_queryset(self):
        """
        过滤数据集
        :return: querySet
        """
        self.get_query_params()
        if self.params_dict:
            if self.sort:
                queryset = self.queryset.filter(**self.params_dict).order_by(self.sort)
            else:
                queryset = self.queryset.filter(**self.params_dict)
        else:
            queryset = self.queryset
        return queryset

    def list(self, request, *args, **kwargs):
        """
        列出所有的Station信息
        :param request: GET /api/manage/station
        :param args:
        :param kwargs:
        :return: json
        """
        queryset = self.get_queryset()
        if queryset.exists():
            ret_page = self.pagination.paginate_queryset(queryset, request, self)
            passenger_serializer = self.serializer_class(ret_page, many=True)
            context = {
                'code': 2000,
                'message': '获取数据成功',
                'total': queryset.count(),
                'data': passenger_serializer.data
            }
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
        创建新的Station数据
        :param request: POST /api/manage/station
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        form = self.get_request_data()
        if self.valid_station_data(form):
            try:
                new_station = Station(**form)
                new_station.save()
                context['code'] = 2000
                context['message'] = '创建数据成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '创建数据失败, 出现错误{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '数据不符合规范'
        return Response(context)

    def update(self, request, *args, **kwargs):
        """
        更新Station数据
        :param request: PUT /api/manage/station
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        sid = self.request.data.get('station_id', None)
        if sid:
            queryset = self.get_queryset().filter(station_id=sid)
            if queryset.exists():
                form = self.get_request_data()
                # TODO: 数据格式验证
                try:
                    queryset.update(**form)
                    context['code'] = 2000
                    context['message'] = '数据更新成功'
                    context['data'] = list(queryset.values())
                except BaseException as e:
                    context['code'] = 2000
                    context['message'] = '数据更新失败,{}'.format(e)
            else:
                context['code'] = 1000
                context['message'] = '不存在指定数据'
        else:
            context['code'] = 1000
            context['message'] = '不存在指定数据'
        return Response(context)

    def destroy(self, request, *args, **kwargs):
        """
        删除Station数据
        :param request: DELETE /api/manage/station
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        sid = self.request.data.get('station_id', None)
        if sid:
            try:
                station = Station.objects.get(station_id=sid)
                station.delete()
                context['code'] = 2000
                context['message'] = '删除成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '删除失败，{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '删除失败'
        return Response(context)
