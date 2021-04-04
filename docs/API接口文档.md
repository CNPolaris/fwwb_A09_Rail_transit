

## API接口文档 V1.5.7

### 前后端数据交互约定

### 用户管理

#### 用户登录

###### 请求消息

```http
POST /api/userprofile/login HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body中参数以格式json存储

需要携带如下参数

- `username` 用户名
- `password` 密码

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储

如果登录成功，返回如下

```json
{
    "code":2000,
    "data":{'token':token}
}
```

- data.token为前后端交互需要使用的令牌

- `code`为2000表示登录成功

如果登录失败，返回登录失败的原因，示例如下

```json
{
    "code": 1000,    
    "message":  "用户名或者密码错误"
}
```

- `code`为 1000 表示登录失败
-  `message`字段描述登录失败的原因

#### 用户登出

###### 请求消息

###### 请求参数

###### 响应消息

###### 响应内容

#### 用户信息

##### 获取信息

###### 请求消息

###### 请求参数

###### 响应消息

###### 响应内容

##### 修改信息

###### 请求消息

###### 请求参数

###### 响应消息

###### 响应内容

#### 权限管理

##### 修改权限

###### 请求消息

###### 请求参数

###### 响应消息

###### 响应内容

##### 赋予权限

###### 请求消息

###### 请求参数

###### 响应消息

###### 响应内容

### 数据管理

#### 出行记录

##### 列出所有出行记录

###### 请求消息

```http
GET /api/manage/trip/list?action=list_trip HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，（多参数之间通过&连接）

- action
  
  - 填写值为`list_trip`
- token字段必须携带，用于后端验证权限
- url可以携带其他参数如
  - id\uid\station\date\channel\price
- page参数为空时，默认为1
- limit参数为空时，默认为40
- sort参数携带用于对数据进行排序的字段 

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type :application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果获取信息成功，返回如下

```json
{
    "code": 2000,
    "data":[
        {
            "id": 1,
            "uesr_id": "d4ec5a712f2b24ce226970a8d315dfce",
            "in_station": "Sta18",
            "in_station_time": "2020-07-15 14:21:58.000000",
            "out_station": "Sta9",
            "out_station_time": "2020-07-15 14:39:29.000000",
            "channel": 3,
            "price": 200
        },
        {
            "id": 2,
            "uesr_id": "d4ec5a712f2b24ce226970a8d315dfce",
            "in_station": "Sta18",
            "in_station_time": "2020-07-15 14:21:58.000000",
            "out_station": "Sta9",
            "out_station_time": "2020-07-15 14:39:29.000000",
            "channel": 3,
            "price": 200
        }
    ]
}
```

- `code`为2000表示获取数据成功

如果获取信息失败，返回如下

```json
{
    "code": 1000,
    "message":"获取数据失败"
}
```

- `code`为1000表示获取数据失败
- `message`返回出现错误的原因

##### 添加一个出行记录

###### 请求消息

```http
POST /api/manage/trip/create?action=add_trip HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加出行记录的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"add_trip",   
    "user_id":"d4ec5a712f2b24ce226970a8d315dfce",
    "in_station": "Sta18",
    "in_station_time": "2020-07-15 14:21:58.000000",
    "out_station": "Sta9",
    "out_station_time": "2020-07-15 14:39:29.000000",
    "channel": 3,
    "price": 200
}
```

- token 字段为用户请求数据需要携带的令牌
- action 字段指明要进行的业务，用于业务转发
- user_id, in_station,in_station_time,out_station,out_station_time,channel,price等为要增加的数据项的内容

服务端在接受到该请求后，应当在验证权限、确认数据格式正确后在系统中添加这样一条记录

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息在body中，数据以json格式存储，

如果添加成功，返回如下

```json
{
	"code":2000
}
```

- `code`为2000表示添加成功

如果添加失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"该记录已经存在"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

##### 修改一个出行记录

###### 请求消息

```http
PUT /api/manage/trip/update HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改客户的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"modify_trip",
    "id":6,
    "user_id":"d4ec5a712f2b24ce226970a8d315dfce",
    "in_station": "Sta18",
    "in_station_time": "2020-07-15 14:21:58.000000",
    "out_station": "Sta9",
    "out_station_time": "2020-07-15 14:39:29.000000",
    "channel": 3,
    "price": 200
}
```

- token 字段为用户请求数据需要携带的令牌
- action 字段指明要进行的业务，用于业务转发
- user_id, in_station,in_station_time,out_station,out_station_time,channel,price等为要修改的数据项的内容

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储

如果修改成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"数据不全"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

##### 删除一个出行记录

###### 请求消息

```http
DELETE /api/manage/trip/delete HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"del_trip",
    "id":888
}
```

- token 字段为用户请求数据需要携带的令牌
- action 字段固定填写del_trip表示删除一条记录，用于业务转发
- id字段为要删除的记录id号

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果删除成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"id为888的记录不存在"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

#### 站点信息

##### 列出所有站点记录

###### 请求消息

```http
GET /api/manage/station/list HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，

- action为list_station,表明是列出所有的站点信息，用于业务转发
- token 用于权限验证的令牌
- 可以携带station_id\station_name\station_route\admin_area等参数

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type :application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果获取信息成功，返回如下

```json
{
    "code": 2000,
    "data":[
        {
            "station_id": 1004,
            "station_name": "Sta18",
            "station_route": "1号线",
            "admin_area":"Dist1"
        },
        {     
            "station_id": 1006,
            "station_name": "Sta159",
            "station_route": "1号线",
            "admin_area":"Dist1"
        }
    ]
}
```

##### 添加一个站点

###### 请求消息

```http
POST /api/manage/station/create HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加出行记录的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"add_station",
    "station_id": 1006,
    "station_name": "Sta159",
    "station_route": "1号线",
    "admin_area":"Dist1"
}
```

- token 为用于权限验证的令牌
- action字段固定填写`add_station`表示添加一个出行记录,用于业务转发

- 其余字段中存储了要添加的站点的信息

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息在body中，数据以json格式存储，

如果添加成功，返回如下

```json
{
	"code":2000
}
```

- `code`为2000表示添加成功

如果添加失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"该记录已经存在"
}
```

- `ret`为1000表示失败
- `message`字段描述添加失败的原因

##### 修改一个站点信息

###### 请求消息

```http
PUT /api/manage/station/update HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改客户的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"modify_station",
    "station_id": 1006,
    "station_name": "Sta159",
    "station_route": "1号线",
    "admin_area":"Dist1"
}
```

- token 为用于权限验证的令牌
- action字段固定填写modify_station表示修改一条出行记录的信息

- station_id字段为要修改的记录的id号

- 其余字段中存储了修改后的站点的信息

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储

如果修改成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示修改成功成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"数据不全"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

##### 删除一个站点信息

###### 请求消息

```http
DELETE /api/manage/station/delete HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"del_station",
    "station_id":888
}
```

- token 为用于权限验证的令牌
- action字段固定填写del_station表示删除一条记录
- station_id字段为要删除的站点的id

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果删除成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示删除成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"id为888的记录不存在"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

#### 工作日信息

##### 列出所有工作日信息

###### 请求消息

```http
GET /api/manage/workday/list?action=list_workday HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，

- action
  - 填写值为list_workday
- token 用于权限验证的令牌
- 可以携带date\cls参数

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type :application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果获取信息成功，返回如下

```json
{
    "code": 2000,
    "data":[
        {
			"date":"2019-12-31",
            "date_class":3
        },
        {
			"date":"2019-01-01",
            "date_class":1
        }
    ]
}
```

如果获取数据失败，返回如下

```json
{
    "code":1000,
    "message":"获取失败的原因"
}
```

##### 添加一个工作日信息

###### 请求消息

```http
POST /api/manage/workday/create HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加出行记录的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"add_workday",
    "date":"2019-12-31",
    "date_class":3
}
```

- token 用于权限验证的令牌
- action字段固定填写`add_workday`表示添加一个出行记录

- 其他字段中存储了要添加的出行记录的信息

服务端在接受到该请求后，应当在验证权限后在系统中添加这样一条记录

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息在body中，数据以json格式存储，

如果添加成功，返回如下

```json
{
	"code":2000
}
```

- `code`为2000表示添加成功

如果添加失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"该记录已经存在"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

##### 修改一个工作日记录

###### 请求消息

```http
PUT /api/manage/workday/update HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改客户的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"modify_workday",
    "date":"2020-01-01",
	"date_class":1
}
```

- token 用于权限验证的令牌

- action字段固定填写modify_workday表示修改一条出行记录的信息

- date字段为要修改的记录的日期

- date_class字段中存储了修改后的信息

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储

如果修改成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"数据不全"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

##### 删除一个工作日记录

###### 请求消息

```http
DELETE /api/manage/workday/delete HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"del_workday",
    "date":"2020-01-01"
}
```

- token 用于权限验证的令牌
- action字段固定填写del_workday表示删除一条记录

- date字段为要删除的记录的日期

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果删除成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"id为2020-01-01,的记录不存在"
}
```

- `code`不为0表示失败
- `message`字段描述添加失败的原因

#### 乘客信息

##### 列出所有出行乘客的信息

###### 请求消息

```http
GET /api/manage/passenger?action=list_passenger HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，

- action
  - 填写值为list_passenger
- token 用于权限验证的令牌
- 可以携带其他参数如passenger_id.dist,birth,gender

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type :application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果获取信息成功，返回如下

```json
{
    "code": 2000,
    "data":[
        {
            "uesr_id": "d4ec5a712f2b24ce226970a8d315dfce",
            "dist": 5105,
            "brith": 1987,
            "gender": 1,
        },
        {
            "uesr_id": "d4ec5a712f2b24ce226970a8d315dfce",
            "dist": 5105,
            "brith": 1988,
            "gender": 0,
        }
    ]
}
```

##### 添加一个乘客信息记录

###### 请求消息

```http
POST /api/manager/passenger/create HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加乘客的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"add_passenger",
    "passenger_id": "d4ec5a712f2b24ce226970a8d315dfce",
    "dist": 5105,
    "brith": 1987,
    "gender": 1,
}
```

- token 用于权限验证的令牌

- action字段固定填写`add_passager`表示添加一个乘客信息记录

- 其他字段中存储了要添加的乘客的信息

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息在body中，数据以json格式存储，

如果添加成功，返回如下

```json
{
	"code":2000
}
```

- `code`为2000表示添加成功

如果添加失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"该记录已经存在"
}
```

- `code`为1000表示失败，
- `message`字段描述添加失败的原因

##### 修改一位乘客记录

###### 请求消息

```http
PUT /api/manage/passenger/update HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改乘客的信息

消息体的格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"modify_trip",
    "passenger_id":"d4ec5a712f2b24ce226970a8d315dfce",
    "dist": 5105,
    "brith": 1987,
    "gender": 1,
}
```

- token 用于权限验证的令牌
- action字段固定填写modify_passager表示修改乘客的信息

- passenger_id字段为要修改的乘客的id号

- 其他字段中存储了修改后的乘客的信息

服务端在接受到该请求后，应该在系统中添加一条这样的信息

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储

如果修改成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"格式不对"
}
```

- `code`为1000表示失败
- `message`字段描述添加失败的原因

##### 删除一条乘客记录

###### 请求消息

```http
DELETE /api/manage/passenger/delete HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "token":"1&z5$cpj_x&y7watx4o3ajs&3k9b7*_46i4j%*%qb+7x5m%t6_",
    "action":"del_passenger",
    "passenger_id":"d4ec5a712f2b24ce226970a8d315dfce"
}
```

- token 用于权限验证的令牌

- action字段固定填写del_passenger表示删除一条记录

- passenger_id字段为要删除的记录id号

服务端在接受到该请求后，应该在系统中尝试删除该id对应的记录。

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果删除成功，返回如下

```json
{
    "code":2000
}
```

- `code`为2000表示成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "code":1000,
    "message":"id为d4ec5a712f2b24ce226970a8d315dfce的记录不存在"
}
```

- `code`为1000表示失败
-  `message`字段描述添加失败的原因

### Echarts数据API

#### 乘客的年龄组成结构

###### 请求消息

```http
GET /api/echarts/agestruct?action=age_struct HTTP /1.1
```

###### 请求参数

http的GET请求参数应当在url路由中

- `action`字段固定填写age_struct表示列出所有的age和birth信息

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息中，数据以json格式存储

如果获取数据成功，示例如下

```http
{
    "code": 2000,
    "data": [
        {
            "name": "0-6",
            "value": 0
        },
        {
            "name": "7-17",
            "value": 535
        },
        {
            "name": "18-40",
            "value": 100799
        },
        {
            "name": "41-65",
            "value": 22983
        },
        {
            "name": "66+",
            "value": 465
        }
    ],
    "name": [
        "0-6",
        "7-17",
        "18-40",
        "41-65",
        "66+"
    ]
}
```

`code`为0表示获取成功

`data`字段为返回的数据

- name 表示年龄区间
- value 表示每个区间内的乘客数量

`name`字段里是前后端约定的分组区间，用于echarts绘制图形

如果请求数据失败，示例如下

```json
{
    "code":1000,
    "message":"年龄组成结构查询结果为空"
}
```

code不为0表示请求数据失败

#### 某天的出行量

###### 请求消息

```http
GET /api/echarts/daily?action=list_daily HTTP/1.1
```

###### 请求参数

http GET请求中，参数应当在url路由中

- aciton=list_daily 固定填写list_daily 表示请求列出所有日期的出行量
- date字段固定填写需要获取数据所在的时间,如date=2020-01-01，列出当日的出行量

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息体中，数据以json格式存储

如果获取数据成功，示例如下

```json
{
    "code": 2000,
    "data": [
        {
            "date": "2020-07-16",
            "count": 7477
        },
        {
            "date": "2020-07-15",
            "count": 7494
        }
}
```

如果获取失败，示例如下

```json
{
    "code": 1000,
    "message": "不支持该类型的http访问"
}
```

#### 单月整体客流量

###### 请求消息

```http
GET /api/echarts/month?action=list_month HTTP/1.1
```

###### 请求参数

- action固定填写list_month 表示列出当年所有月度的客流量
- date字段用来确定具体月度的每日客流量

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应内容消息体中，数据以json格式存储

如果获取数据成功，示例如下

```json
{
    "code": 2000,
    "data": [
        {
            "date": "2020-04-30",
            "count": 6191
        },
        {
            "date": "2020-04-29",
            "count": 5473
        }
}
```

如果获取数据失败，示例如下

```json
{
    "code": 1000,
    "msg": "不支持该类型的http请求"
}
```

#### 站点OD客流分析

###### 请求消息

```http
GET /api/echarts/od?action=list_od HTTP/1.1
```

###### 请求参数

- http请求消息body参数action固定填写list_od,表示默认列出所有站点的OD客流分析
- http请求消息body中携带参数
  - station 要检索的站点
  - date 要检索的时间

具体的消息格式为json，示例如下

```json
{
    "action":"list_od",
    "station":"Sta188",
    "date":"2020-01-01 09:08:01"
}
```

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type:application/json
```

###### 响应内容

http响应内容中，数据以json格式存储

如果获取数据成功，示例如下

```json
{
    "code": 2000,
    "data": [
        {
            "in_station": "Sta65",
            "out_station": "Sta104",
            "count": 18
        },
        {
            "in_station": "Sta110",
            "out_station": "Sta63",
            "count": 15
        }        
}
```

如果获取数据失败，示例如下

```json
{
    "code":1000,
    "message":"获取数据失败"
}
```

#### 实时客流数据获取

##### 单站点出入客流

###### 请求消息

```http
GET /api/echarts/realtime?action=station_of_point HTTP/1.1
```

###### 请求参数

http请求参数在消息体中，格式为json,示例如下

```json
{
    "date":"2020-01-01",
    "station":""
}
```

- action为固定填写参数，表明所要指定完成的事务
- date字段为固定填写时间
- station字段固定填写指定的站点

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息body中，数据以json格式存储，

如果获取信息成功，返回如下

```json
{
    "code": 2000,
    "in_list": [],
    "out_list": [
        {
            "hour": 14,
            "count": 1
        },
        {
            "hour": 15,
            "count": 1
        }
    ]
}
```

如果获取信息失败，返回如下

```json
{
    "code": 1000,
    "message": "请求消息不全"
}
```

### 数据导出API

######  请求消息

```http
GET /api/exports?model=station HTTP/1.1
```

###### 请求参数

http请求消息在url中，参数model固定填写要导出的目标model，不可为空

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type:application/octet-stream
```

###### 响应内容

如果数据能够成功导出，应会返回下载选项

如果数据无法导出，消息以json格式存储，示例如下

```json
{
    'code': 1000,
    'msg': '需要高级管理员权限才可导出数据',
    'redirect': '/sign.html'
}
```











