## fwwb_A09_Rail_transit💯

> 基于Django，JWT，Vue & Element 的前后端分离的轨道交通客流预测系统

### 项目介绍

- 前端采用Vue\Element UI
- 后端采用Django\JWT
- 权限认证使用JWT
- 特别鸣谢 [element](https://github.com/ElemeFE/element)\\[vue-element-admin](https://github.com/PanJiaChen/vue-element-admin)

### 内置功能

### 在线体验😺

- admin/123456

演示地址: [演示地址](http://47.117.118.196:8080/)

文档地址:[文档地址](https://space-9358y2.w.eolinker.com/#/share/index?shareCode=18VfD2)

### 部署教程😽

> 基于CentOS7

#### 后端部分

首先为后端准备虚拟环境

```shell
~$ sudo yum install python3
~$ sudo yum install python3-pip
~$ sudo pip3 install virtualenv
```

接下来修改后端的配置文件`settings.py`

```python
# fwwb_A09_Rail_transit/settings.py

# 关闭调试模式
DEBUG = False
# 配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '', # 你的数据库名
        'USER': '', # 用户名
        'PASSWORD': '', # 密码
        'HOST': '', # host
        'PORT': '3306', # 端口
    }
}
# 允许的服务器
ALLOWED_HOSTS = ['*']
```

在项目根目录下创建虚拟环境\安装库\数据迁移

1. 创建并进入虚拟环境

   ```shell
   $ virtualenv --python=python3.6 venv
   $ source venv/bin/activate
   (venv)$ 
   ```

2. 安装库

   ```shell
   (venv) $ pip3 install -r requirements.txt
   ```

   **注意**: 可能存在部分包的版本不对,原因是开发时是在win下进行的,Linux下相同的包的版本可能存在不一致,只需删除`requirements.txt`中存在问题的包的版本后缀即可

3. 数据迁移

   ```shell
   (venv) $ python manage.py makemigrations
   (venv) $ python manage.py migrate
   ```

4. 以上基础工作完成后就可以启动后端服务了

    ```shell
    (venv) $ pip3 install gunicorn
    (venv)gunicorn fwwb_A09_Rail_transit.wsgi:application --bind 0.0.0.0:8090
    ```

     通过gunicorn将服务绑定在0.0.0.0:8090端口

#### 前端部分

[前端项目](https://gitee.com/cnpolaris-tian/vue-element-admin.git)

通过执行以下代码对前端项目进行打包得到静态文件

```sh
# 打包正式环境
npm run build:prod

# 打包预发布环境
npm run build:stage
```

构建打包成功之后，会在根目录生成 `dist` 文件夹，里面就是构建打包好的文件，通常是 `***.js` 、`***.css`、`index.html` 等静态文件。

如果需要自定义构建，比如指定 `dist` 目录等，则需要通过 [config](https://github.com/PanJiaChen/vue-element-admin/blob/master/vue.config.js)的 `outputDir` 进行配置

将打包得到的`dist`文件夹压缩传到服务器上的后端项目的根目录下

接下来通过`Nginx`驱动前端

安装`nginx`

```sh
~$ sudo yum install nginx
~$ cd etc/nginx/
~$ sudo vi nginx.conf
```

```
user root;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80;
        server_name  47.117.118.196;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
 		root         /root/cnpolaris/myprojects/fwwb_A09_Rail_transit/dist;
		index index.html index.htm;
        }

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
   }
}
```

此配置会监听 80 端口（通常 http 请求的端口），监听的 IP 地址写你自己的**服务器公网 IP**

```sh
# 启动Nginx
service nginx start
# 每次修改配置文件后
service nginx restart
```

此时已经可以通过ip看到前端内容了,但是前后端还尚未关联,接下来继续修改nginx.conf

#### 关联前后端

在nginx.conf的server中添加

```
location /api {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $http_host;
    proxy_pass http://0.0.0.0:8090;
}
```

当请求前端请求api时,会自动转发给后端进行处理

### 进程托管

为了避免当 SSH 终端一关闭，Web 服务也一起被关闭了，导致网站无法连接,需要进行进程托管.

参考@frostming 的文章[<Web服务的进程托管>](https://frostming.com/2020/05-24/process-management/)

1. 在项目根目录下建立run.sh文件

```sh
$ vi run.sh
```

```sh
#!/bin/bash
source /root/cnpolaris/myprojects/fwwb_A09_Rail_transit/venv/bin/activate 
cd /root/cnpolaris/myprojects/fwwb_A09_Rail_transit
gunicorn fwwb_A09_Rail_transit.wsgi:application --bind 0.0.0.0:8090
```

2. 在/etc/systemd/system/ 目录下创建一个transit.service 进程文件

   ```sh
   [Unit]
   Description=fwwb transit service
   
   [Service]
   Type=forking
   ExecStart=/bin/bash /root/cnpolaris/myprojects/fwwb_A09_Rail_transit/run.sh
   KillMode=process
   Restart=on-failure
   RestartSec=3s
   [Install]
   WantedBy=multi-user.target
   ```

   ```
   systemctl enable transit
   ```

### 演示图

![](https://gitee.com/cnpolaris-tian/giteePagesImages/raw/master/null/20210430170529.png)

![](https://gitee.com/cnpolaris-tian/giteePagesImages/raw/master/null/20210430170618.png)

![](https://gitee.com/cnpolaris-tian/giteePagesImages/raw/master/null/image-20210430170641760.png)

![](https://gitee.com/cnpolaris-tian/giteePagesImages/raw/master/null/20210430170836.png)