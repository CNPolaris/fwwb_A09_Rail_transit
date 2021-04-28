from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from userprofile.models import Profile
from userprofile.permissions import IsAdminUserOrReadOnly
from userprofile.serializers import UserSerializer, UserProfileSerializer
from django.core.paginator import Paginator


class UserManageViveSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination = Paginator
    params_dict = {}
    limit = 20
    page = 1
    sort = None

    def get_permissions(self):
        """
        验证请求用户的权限 admin才可以进行操作
        :return: []
        """
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUserOrReadOnly]

        return super().get_permissions()

    def get_query_params(self):
        """
        解析请求用户管理的请求参数
        :return: dict
        """
        self.params_dict = self.request.query_params.dict()
        if 'token' in self.params_dict.keys():
            del self.params_dict['token']
        if 'page' in self.params_dict.keys():
            self.page = self.params_dict['page']
            del self.params_dict['page']
        if 'limit' in self.params_dict.keys():
            self.limit = self.params_dict['limit']
            del self.params_dict['limit']
        if 'sort' in self.params_dict.keys():
            del self.params_dict['sort']

        self.sort = self.request.query_params.get('sort', None)

    def get_queryset(self):
        """
        过滤User数据集
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
        列出符合的User信息
        :param request: GET /api/permission
        :param args:
        :param kwargs:
        :return: json
        """
        queryset = self.get_queryset()
        if queryset.exists():
            paginator = self.pagination(queryset.values('id', 'username', 'is_superuser', 'profile__roles',
                                                        'profile__online', 'email', 'profile__phone', 'last_login',
                                                        'is_active',
                                                        'profile__introduction'), self.limit)
            page = paginator.page(self.page)
            context = {
                'code': 2000,
                'total': queryset.count(),
                'data': list(page)
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

    def update(self, request, *args, **kwargs):
        """
        更新用户信息
        :param request:PUT /api/permission/
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        uid = self.request.data.get('id', None)
        if uid:
            if self.queryset.get(id=uid):
                queryset = self.queryset.get(id=uid)

                introduction = self.request.data.get('introduction', None)
                if introduction:
                    queryset.profile.introduction = introduction
                user_name = self.request.data.get('username', None)
                email = self.request.data.get('email', None)
                if user_name is not None:
                    queryset.username = user_name
                if email is not None:
                    queryset.email = email

                queryset.save()
                context['code'] = 2000
                context['message'] = '数据更新成功'
            else:
                context['code'] = 1000
                context['message'] = '不存在指定数据'
        else:
            context['code'] = 1000
            context['message'] = '不存在指定数据'
        return Response(context)

    def destroy(self, request, *args, **kwargs):
        """
        删除用户
        :param request: DELETE /api/permission/
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        uid = self.request.data.get('id', None)
        if uid:
            try:
                delete_user = self.queryset.get(id = uid)
                delete_user.delete()
                context['code'] = 2000
                context['message'] = '用户删除成功'
            except BaseException as e:
                context['code'] = 1000
                context['message'] = '删除失败,出现错误{}'.format(e)
        else:
            context['code'] = 1000
            context['message'] = '不存在该用户'
        return Response(context)

    def create(self, request, *args, **kwargs):
        """
        创建用户
        :param request: POST /api/permission/
        :param args:
        :param kwargs:
        :return: json
        """
        context = {}
        # 提取数据
        user_name = self.request.data.get('username')
        password = self.request.data.get('password')
        email = self.request.data.get('email')
        role = self.request.data.get('role')
        introduction = self.request.data.get('introduction')
        phone = self.request.data.get('phone')
        online = 0
        avatar = 'https://gitee.com/cnpolaris-tian/giteePagesImages/raw/master/null/IMG_7777(20200409-144633).JPG'

        try:
            user = User.objects.create_user(username=user_name, password=password, email=email)

            profile = Profile.objects.get(user=user)
            profile.roles = role
            profile.introduction = introduction
            profile.online = online
            profile.avatar = avatar
            profile.phone = phone
            profile.save()
        except BaseException as e:
            context['code'] = 1000
            context['message'] = '用户名重复请重新输入'
        context['code'] = 2000
        context['message'] = "创建新用户成功"
        return Response(context)
