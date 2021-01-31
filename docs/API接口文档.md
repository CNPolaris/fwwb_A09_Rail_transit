## API接口文档 V1.0.1

### 登陆系统

###### 请求消息

###### 请求参数

###### 响应消息

###### 响应内容

### 系统数据API

#### 出行记录

##### 列出所有出行记录

###### 请求消息

```http
GET /api/manager/trips?action=list_trip HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，（多参数之间通过&连接）

- action
  
  - 填写值为`list_trip`
  - url可以携带其他参数如
    - id\uid\station\date\channel\price
  
  - page参数必须携带，否则默认只返回第一页数据

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
    "ret": 0,
    "retlist":[
        {
            "id": 1,
            "uesr_id": "d4ec5a712f2b24ce226970a8d315dfce",
            "in_station": "Sta18",
            "in_station_time": "2020-07-15 14:21:58.000000",
            "out_station": "Sta9",
            "out_station_time": "2020-07-15 14:39:29.000000",
            "channel": 3,
            "pricr": 200
        },
        {
            "id": 2,
            "uesr_id": "d4ec5a712f2b24ce226970a8d315dfce",
            "in_station": "Sta18",
            "in_station_time": "2020-07-15 14:21:58.000000",
            "out_station": "Sta9",
            "out_station_time": "2020-07-15 14:39:29.000000",
            "channel": 3,
            "pricr": 200
        }
    ]
}
```



##### 添加一个出行记录

###### 请求消息

```http
POST /api/manager/trips HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加出行记录的信息

消息体的格式是json，如下示例：

```json
{
    "action":"add_trip",
    "data":{
        "user_id":"d4ec5a712f2b24ce226970a8d315dfce",
        "in_station": "Sta18",
        "in_station_time": "2020-07-15 14:21:58.000000",
        "out_station": "Sta9",
        "out_station_time": "2020-07-15 14:39:29.000000",
        "channel": 3,
        "price": 200
    }
}
```

**注意**：**action字段固定填写`add_trip`表示添加一个出行记录**

**data字段中存储了要添加的出行记录的信息**

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
	"ret":0,
	"id":188
}
```

`ret`为0表示添加成功

`id`为添加记录的id号

如果添加失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"该记录已经存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

##### 修改一个出行记录

###### 请求消息

```http
PUT /api/manager/trips HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改客户的信息

消息体的格式是json，如下示例：

```json
{
    "action":"modify_trip",
    "id":6,
    "newdata":{
        "user_id":"d4ec5a712f2b24ce226970a8d315dfce",
        "in_station": "Sta18",
        "in_station_time": "2020-07-15 14:21:58.000000",
        "out_station": "Sta9",
        "out_station_time": "2020-07-15 14:39:29.000000",
        "channel": 3,
        "pricr": 200
    }
}
```

**注意：**action字段固定填写modify_trip表示修改一条出行记录的信息

id字段为要修改的记录的id号

newdata字段中存储了修改后的出行记录的信息

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
    "ret":0
}
```

`ret`为0表示成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"数据不全"
}
```

`ret`不为0表示失败,`msg`字段描述添加失败的原因

##### 删除一个出行记录

###### 请求消息

```http
DELETE /api/manager/trips HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "action":"del_trip",
    "id":888
}
```

**注意**：action字段固定填写del_trip表示删除一条记录

id字段为要删除的记录id号

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
    "ret":0
}
```

`ret`为0表示成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"id为888的记录不存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

#### 站点信息

##### 列出所有站点记录

###### 请求消息

```http
GET /api/manager/station?action=list_station HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，

- action
  - 填写值为list_station
- 可以携带sid\name\route\area等参数

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
    "ret": 0,
    "retlist":[
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
POST /api/manager/station HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加出行记录的信息

消息体的格式是json，如下示例：

```json
{
    "action":"add_station",
    "data":{
        "station_id": 1006,
        "station_name": "Sta159",
        "station_route": "1号线",
        "admin_area":"Dist1"
    }
}
```

**注意**：**action字段固定填写`add_station`表示添加一个出行记录**

**data字段中存储了要添加的站点的信息**

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
	"ret":0,
	"id":188
}
```

`ret`为0表示添加成功

`id`为添加记录的id号

如果添加失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"该记录已经存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

##### 修改一个站点信息

###### 请求消息

```http
PUT /api/manager/station HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改客户的信息

消息体的格式是json，如下示例：

```json
{
    "action":"modify_station",
    "sid":6,
    "newdata":{
        "station_id": 1006,
        "station_name": "Sta159",
        "station_route": "1号线",
        "admin_area":"Dist1"
    }
}
```

**注意：**action字段固定填写modify_station表示修改一条出行记录的信息

sid字段为要修改的记录的id号

newdata字段中存储了修改后的站点的信息

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
    "ret":0
}
```

`ret`为0表示成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"数据不全"
}
```

`ret`不为0表示失败,`msg`字段描述添加失败的原因

##### 删除一个站点信息

###### 请求消息

```http
DELETE /api/manager/station HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "action":"del_station",
    "sid":888
}
```

**注意**：action字段固定填写del_station表示删除一条记录

id字段为要删除的记录id号

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
    "ret":0
}
```

`ret`为0表示成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"id为888的记录不存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

#### 工作日信息

##### 列出所有工作日信息

###### 请求消息

```http
GET /api/manager/workday?action=list_workday HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，

- action
  - 填写值为list_workday
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
    "ret": 0,
    "retlist":[
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

##### 添加一个工作日信息

###### 请求消息

```http
POST /api/manager/workday HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加出行记录的信息

消息体的格式是json，如下示例：

```json
{
    "action":"add_workday",
    "data":{
        "date":"2019-12-31",
        "date_class":3
    }
}
```

**注意**：**action字段固定填写`add_workday`表示添加一个出行记录**

**data字段中存储了要添加的出行记录的信息**

服务端在接受到该请求后，应当在验证权限后在系统中添加这样一条记录

###### 响应消息

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

###### 响应内容

http响应消息在body中，数据以json格式存储，

如果添加成功，返回如下

```http
{
	"ret":0,
	"date":"2020-01-01",
	"date_class":1
}
```

`ret`为0表示添加成功

`date`为添加的日期

`date_class`为添加的日期的属性

如果添加失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"该记录已经存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

##### 修改一个工作日记录

###### 请求消息

```http
PUT /api/manager/workday HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改客户的信息

消息体的格式是json，如下示例：

```json
{
    "action":"modify_workday",
    "date":"2020-01-01",
    "newdata":{
	"date_class":1
    }
}
```

**注意：**action字段固定填写modify_workday表示修改一条出行记录的信息

id字段为要修改的记录的日期

newdata字段中存储了修改后的信息

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
    "ret":0
}
```

`ret`为0表示成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"数据不全"
}
```

`ret`不为0表示失败,`msg`字段描述添加失败的原因

##### 删除一个工作日记录

###### 请求消息

```http
DELETE /api/manager/workday HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "action":"del_workday",
    "date":"2020-01-01"
}
```

**注意**：action字段固定填写del_workday表示删除一条记录

id字段为要删除的记录的日期

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
    "ret":0
}
```

`ret`为0表示成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"id为2020-01-01,的记录不存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

#### 乘客信息

##### 列出所有出行乘客的信息

###### 请求消息

```http
GET /api/manager/passager?action=list_passager HTTP/1.1
```

###### 请求参数

http请求消息url中需要携带如下参数，

- action
  - 填写值为list_passager

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
    "ret": 0,
    "retlist":[
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
POST /api/manager/passager HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带添加乘客的信息

消息体的格式是json，如下示例：

```json
{
    "action":"add_passager",
    "data":{
            "uesr_id": "d4ec5a712f2b24ce226970a8d315dfce",
            "dist": 5105,
            "brith": 1987,
            "gender": 1,
    }
}
```

**注意**：**action字段固定填写`add_passager`表示添加一个乘客信息记录

**data字段中存储了要添加的乘客的信息**

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
	"ret":0,
	"id":188
}
```

`ret`为0表示添加成功

`id`为添加的乘客的id

如果添加失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"该记录已经存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

##### 修改一位乘客记录

###### 请求消息

```http
PUT /api/manager/passager HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http请求消息body携带修改乘客的信息

消息体的格式是json，如下示例：

```json
{
    "action":"modify_trip",
    "id":"d4ec5a712f2b24ce226970a8d315dfce",
    "newdata":{
            "dist": 5105,
            "brith": 1987,
            "gender": 1,
    }
}
```

**注意：**action字段固定填写modify_passager表示修改乘客的信息

id字段为要修改的乘客的id号

newdata字段中存储了修改后的乘客的信息

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
    "ret":0
}
```

`ret`为0表示成功

如果修改失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"格式不对"
}
```

`ret`不为0表示失败,`msg`字段描述添加失败的原因

##### 删除一条乘客记录

###### 请求消息

```http
DELETE /api/manager/passager HTTP/1.1
Content-Type: application/json
```

###### 请求参数

http 请求消息body携带要删除记录的id

消息体格式是json，如下示例：

```json
{
    "action":"del_passager",
    "id":"d4ec5a712f2b24ce226970a8d315dfce"
}
```

**注意**：action字段固定填写del_passager表示删除一条记录

id字段为要删除的记录id号

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
    "ret":0
}
```

`ret`为0表示成功

如果删除失败，返回失败的原因，示例如下

```json
{
    "ret":1,
    "msg":"id为d4ec5a712f2b24ce226970a8d315dfce的记录不存在"
}
```

`ret`不为0表示失败，`msg`字段描述添加失败的原因

### Echarts数据API







