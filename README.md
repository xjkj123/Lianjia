# LianJiaSpider速度一分钟1000+

# 前言
+ 利用[此网页](https://sh.lianjia.com/ditu/)接口实现功能 
+ 目前支持的城市 上海 北京 烟台 厦门 长沙 后续会支持更多请把你需要的城市发为Issues我会时常看
+ 作者：Mrx ；WeChat：xwk245776832 ； 邮箱：xjkj123@icloud.com 有任何问题请发邮件 我会尽可能帮助你
+ 此接口通过网页js脚本计算出get所需参数，攻破了此难点，接口调用次数无限，速度不限，上海市100000+数据不会被反爬

# 运行
   
   
+ ### 下载安装

```commandline
pip install LianJiaSpider
```


+ ### 示例代码
+ ##### 地区区域范围数据库准备
```python

import Lianjia.lianjia as lj

lj.SaveCityBorderIntoDB('上海')

#保存上海市的所有区域边缘经纬度并保存在目录下district.db文件内

```
+ ##### district.db文件表结构如下


```sql
create table 城市名 
(
  id int PRIMARY KEY ,
  name text,
  longitude text,
  latitude text,
  border text,
  unit_price int,
  count int
)
```
+ ##### 1.2.2 爬取区域内二手房楼盘数据

```python
import Lianjia.lianjia as lj

#lj.SaveCityBorderIntoDB('上海')
lj.HoleCityDown('上海')
#保存市区内所有在售楼盘的信息并保存在目录下LianJia_area.db文件内

```
+ ##### LianJia_area.db文件表结构如下


```
create table 城市名 
(
  id int PRIMARY KEY ,
  district text,
  name text,
  longitude text,
  latitude text,
  unit_price int,
  count int
)

```
+ ##### 1.2.3 爬取区域内楼盘中每个在售房屋的信息

```python
import Lianjia.lianjia as lj

#lj.SaveCityBorderIntoDB('上海')
#lj.HoleCityDown('上海')
lj.GetCompleteHousingInfo('上海')

#保存所有在售楼盘的每套房屋信息并保存在目录下DetailInfo.db文件内

```
+ ##### DetailInfo.db文件表结构如下
```

create table 城市名 
(houseId PRIMARY  KEY , 
houseCode, title, appid, 
source, imgSrc, layoutImgSrc, 
imgSrcUri,layoutImgSrcUri, 
roomNum, square, buildingArea, 
buildYear, isNew, ctime,
mtime, orientation, floorStat, 
totalFloor, decorateType, 
hbtName,isYezhuComment, 
isGarage, houseType, isFocus, 
status, isValid, signTime,
signSource, signSourceCn, 
isDisplay, address, community, 
communityId,communityName, 
communityUrl, communityUrlEsf, 
districtId, districtUrldistrictName, 
regionId, regionUrl, regionName, 
bbdName, bbdUrl, houseCityId,
subwayInfo, schoolName, schoolArr, 
bizcircleFullSpell, house_video_info , 
price,unitPrice, viewUrl, listPrice, 
publishTime, isVilla, villaNoFloorLevel,
villaName, tags)

```
+ ### 以上1.2.1，1.2.2，1.2.3 请依次执行，否则会出现错误

+ ### 或者直接运行以下代码，但耗时会很久
```python

import Lianjia.lianjia as lj
city='上海'
lj.SaveCityBorderIntoDB(city)
lj.HoleCityDown(city)
lj.GetCompleteHousingInfo(city)
```
### 2. 高级用法
+ 示例
```
#稍后更新，先写这么多

```


### 3. 版本历史
+ 1.1.0：
> 1. 实现链家地图api协议的逆向实现经纬度区域找房
> 2. 简单上海市区爬虫
+ 1.1.5
> 1. 新增pip，使用此项目可以直接pip install LianJiaSpider安装
> 2. 新增城市



