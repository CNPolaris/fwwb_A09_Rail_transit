# fwwb_A09_Rail_transit

#### 一、介绍
**【问题说明】**     
以地铁 ACC(地铁自动售检票系统清分中心简称)系统的用户行程数据、站点 数据为基础，完成基于地铁出行行程大数据的分析建模和算法研究，实现对地铁 的线路级别以及站点级别的客流进行分析和预测。  
**【用户期望】**     
提供友好的用户交互方式，通过输入或者调整模型的各种相关因子，对指定 时间、指定线路或者站点的客流进行预测和预警并且通过图形化的方式直观展 现。

#### 二、任务清单

1. - [x] 确定技术路线   
   - - [x] 后端技术路线
   - - [x] 前端技术路线
2. - [x] 建立数据库
   - - [x] 优化数据库结构
   - - [ ] 数据分表
3. 基于给定的数据进行客流精确统计
    - [x] 单月整体的客流波动分析
    - [x] 工作日和周末的客流分析
    - [ ] 单站的点出/入站客流分析
    - [x] 用户年龄结构分析
    - [ ] 早晚高峰客流站点分布分析
    - [ ] 站点OD客流量分析
    - [ ] 线路断面（按站点）流量分析
    - [ ] 团队其他自愿拓展的统计分析
4. 建立准确的预测模型
#### 三、使用到的技术
1. 整体架构
B/S结构
2. 后端技术
Django
3. 前端技术
Bootstrap、Jquery、Echarts

#### 四、字典对照

1. 数据字典

   1. users 用户信息

      | 字段    | 说明           | 数据类型 | 字段   | 说明           | 数据类型 |
      | ------- | -------------- | -------- | ------ | -------------- | -------- |
      | user_id | 用户的唯一编号 | varchar  | dist   | 用户所在的省市 | int      |
      | birth   | 用户的出生年份 | int      | gender | 用户的性别     | int      |

   2. station 站点信息

      | 字段          | 说明       | 数据类型 | 字段         | 说明               | 数据类型 |
      | ------------- | ---------- | -------- | ------------ | ------------------ | -------- |
      | station_id    | 站点的编号 | int      | station_name | 站点的名称         | varchar  |
      | station_route | 线路       | varchar  | admin_area   | 站点所在的行政区域 | varchar  |

   3. trips 行程信息

      | 字段            | 说明     | 类型     | 字段             | 说明     | 类型     | 字段    | 说明     | 类型   |
      | --------------- | -------- | -------- | ---------------- | -------- | -------- | ------- | -------- | :----- |
      | in_station      | 入站名   | varchar  | out_station      | 出站名   | varchar  | channel | 购票渠道 | int    |
      | in_station_time | 入站时间 | datetime | out_station_time | 出站时间 | datetime | price   | 票价     | double |
      | user_id_id      | 用户id   | varchar  |                  |          |          |         |          |        |

   4. tripstatistics 实时客流统计

      | 字段  | 说明               | 数据类型 |
      | ----- | ------------------ | -------- |
      | date  | 日期               | date     |
      | count | 每日客流量实时统计 | int      |

   5. workdays 工作日

      | 字段       | 说明             | 数据类型 |
      | ---------- | ---------------- | -------- |
      | date       | 日期             | date     |
      | date_class | 日期所属于的分类 | int      |

      

