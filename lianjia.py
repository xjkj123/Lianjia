import execjs
import requests
import time
import set
import tqdm
import json
import sqlite3
import numpy
import math


def GetCommunityInfo(max_lat, min_lat, max_lng, min_lng, city_id, group_type):
    ###########-----计算authorization值-----############
    time_13 = int(round(time.time() * 1000))
    jsstr = set.js

    ctx = execjs.compile(jsstr)
    authorization = ctx.call('getMd5',
                             {'group_type': group_type, 'city_id': city_id, 'max_lat': max_lat, 'min_lat': min_lat,
                              'max_lng': max_lng, 'min_lng': min_lng, 'request_ts': time_13})
    ###############-----拼接请求url-----#################
    s = set.url % (city_id, group_type, max_lat, min_lat, max_lng, min_lng, '%7B%7D', time_13, authorization, time_13)
    ###############-----发送请求-----#################
    with requests.Session() as sess:
        ret = sess.get(url=s, headers=set.headers, cookies=set.cookies)

        house_json = json.loads(ret.text[43:-1])

        if house_json['errno'] == 0:
            ll = []
            if group_type == 'district':
                return house_json['data']['list']

            if group_type == 'community':
                if type(house_json['data']['list']) is dict:
                    for x in house_json['data']['list']:
                        ll.append(house_json['data']['list'][x])
                    return ll
                else:
                    return house_json['data']['list']
        else:
            return None


def GetHousingInfo(id, count):
    ll = []
    for page in range(1, math.ceil(count / 10) + 1):
        time_13 = int(round(time.time() * 1000))
        jsstr = set.js
        ctx = execjs.compile(jsstr)
        authorization = ctx.call('getMd5', {'filters': "{}", 'id': id, 'order': 0, 'page': page, 'request_ts': time_13})
        ###############-----拼接请求url-----#################
        url = set.url_fang % (id, page, '%7B%7D', time_13, authorization, time_13)

        with requests.Session() as sess:
            ret = sess.get(url=url, headers=set.headers, cookies=set.cookies)
            house_json = json.loads(ret.text[42:-1])

            for x in house_json['data']['ershoufang_info']['list']:
                ll.append(house_json['data']['ershoufang_info']['list'][x])

    return ll


def SaveCityBorderIntoDB(city):  # 读取某市各个区域轮廓
    ret = GetCommunityInfo(max_lat=set.city[city]['max_lat'], min_lat=set.city[city]['min_lat'],
                           max_lng=set.city[city]['max_lng'], min_lng=set.city[city]['min_lng'],
                           group_type='district', city_id=set.city[city]['city_id'])
    conn = sqlite3.connect('district.db')  # 链接数据库
    cursor = conn.cursor()
    try:
        sql = '''create table %s (
                    id int PRIMARY KEY ,
                    name text,
                    longitude text,
                    latitude text,
                    border text,
                    unit_price int,
                    count int
                    )''' % city
        cursor.execute(sql)
    except:
        print('数据表已存在')
    pbar = tqdm.tqdm(ret)
    for x in pbar:
        sql = ''' insert into %s
                          (id, name, longitude,latitude,border,unit_price,count)
                          values
                          (:id, :name, :longitude, :latitude, :border, :unit_price, :count)''' % city
        try:

            cursor.execute(sql, ret[x])

            conn.commit()
            pbar.set_description(ret[x]['name'] + '已导入')
        except:
            pbar.set_description(ret[x]['name'] + '失败')

    cursor.close()
    # for x in numpy.arange(121.118774, 121.944122, 0.1):
    #     for y in numpy.arange(30.820294, 31.487821, 0.1):
    #         print((round(y,6), round(y - 0.1,6), round(x,6), round(x - 0.1,6)))
    #         print(requlianjia(round(y,6), round(y - 0.1,6), round(x,6), round(x - 0.1,6)))


def HoleCityDown(city):  # 爬取小区套数平均价格
    with sqlite3.connect('district.db') as conn:
        c = conn.cursor()
        c.execute('SELECT border,name FROM %s' % city)
        area_list = c.fetchall()
    lat = []
    lng = []
    conn = sqlite3.connect('LianJia_area.db')
    cursor = conn.cursor()
    try:
        sql = '''create table %s (
                        id int PRIMARY KEY ,
                        district text,
                        name text,
                        longitude text,
                        latitude text,
                        unit_price int,
                        count int
                        )
            ''' % city
        cursor.execute(sql)

    except:
        print('数据表已存在')
    for x in area_list:
        district = x[1]
        for y in x[0].split(';'):
            lng.append(float(y.split(',')[0]))
            lat.append(float(y.split(',')[1]))

        li = []
        for x in numpy.arange(min(lng), max(lng), 0.01):
            for y in numpy.arange(min(lat), max(lat), 0.01):
                li.append((round(y, 6), round(y - 0.01, 6), round(x, 6), round(x - 0.01, 6)))
        pbar = tqdm.tqdm(li)
        for x in pbar:
            ret = GetCommunityInfo(x[0], x[1], x[2], x[3], set.city[city]['city_id'], 'community')
            if ret is not None:
                for z in ret:
                    try:
                        sql = ''' insert into %s
                                 (id, name, district,longitude,latitude,unit_price,count)
                                 values
                                 (:id, :name, :district,:longitude, :latitude, :unit_price, :count)
                                 ''' % city
                        z.update({'district': district})
                        cursor.execute(sql, z)
                        conn.commit()

                        pbar.set_description(str(x) + z['name'] + '已导入')
                    except:
                        pbar.set_description(str(x) + z['name'] + '住房已存在')


def GetCompleteHousingInfo(city):  # 爬取所有小区内每个住房信息
    with sqlite3.connect('DetailInfo.db') as conn1:
        cursor1 = conn1.cursor()
        try:
            sql = '''create table %s (houseId PRIMARY  KEY 
            , houseCode, title, appid, source, imgSrc, layoutImgSrc, imgSrcUri,
         layoutImgSrcUri, roomNum, square, buildingArea, buildYear, isNew, ctime,
         mtime, orientation, floorStat, totalFloor, decorateType, hbtName,
         isYezhuComment, isGarage, houseType, isFocus, status, isValid, signTime,
         signSource, signSourceCn, isDisplay, address, community, communityId,
         communityName, communityUrl, communityUrlEsf, districtId, districtUrl,
         districtName, regionId, regionUrl, regionName, bbdName, bbdUrl, houseCityId,
         subwayInfo, schoolName, schoolArr, bizcircleFullSpell, house_video_info , price,
         unitPrice, viewUrl, listPrice, publishTime, isVilla, villaNoFloorLevel,
         villaName, tags)
                ''' % city
            cursor1.execute(sql)



        except:
            print('数据表已存在')

    with sqlite3.connect('LianJia_area.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id,count FROM %s' % city)
        area_list = c.fetchall()
    pbar = tqdm.tqdm(area_list)
    for x in pbar:
        ret = GetHousingInfo(x[0], x[1])
        with sqlite3.connect('DetailInfo.db') as conn:
            cursor=conn.cursor()
            for y in ret:
                try:
                    sql = '''insert into %s(houseId,houseCode,title,appid,source,imgSrc,layoutImgSrc,imgSrcUri,layoutImgSrcUri,roomNum,square,buildingArea,buildYear,isNew,ctime,mtime,orientation,floorStat,totalFloor,decorateType,hbtName,isYezhuComment,isGarage,houseType,isFocus,status,isValid,signTime,signSource,signSourceCn,isDisplay,address,community,communityId,communityName,communityUrl,communityUrlEsf,districtId,districtUrl,districtName,regionId,regionUrl,regionName,bbdName,bbdUrl,houseCityId,subwayInfo,schoolName,schoolArr,bizcircleFullSpell,house_video_info,price,unitPrice,viewUrl,listPrice,publishTime,isVilla,villaNoFloorLevel,villaName,tags)values(:houseId,:houseCode,:title,:appid,:source,:imgSrc,:layoutImgSrc,:imgSrcUri,:layoutImgSrcUri,:roomNum,:square,:buildingArea,:buildYear,:isNew,:ctime,:mtime,:orientation,:floorStat,:totalFloor,:decorateType,:hbtName,:isYezhuComment,:isGarage,:houseType,:isFocus,:status,:isValid,:signTime,:signSource,:signSourceCn,:isDisplay,:address,:community,:communityId,:communityName,:communityUrl,:communityUrlEsf,:districtId,:districtUrl,:districtName,:regionId,:regionUrl,:regionName,:bbdName,:bbdUrl,:houseCityId,:subwayInfo,:schoolName,:schoolArr,:bizcircleFullSpell,:house_video_info,:price,:unitPrice,:viewUrl,:listPrice,:publishTime,:isVilla,:villaNoFloorLevel,:villaName,:tags)''' % city
                    y['house_video_info'] = str(y['house_video_info'])
                    y['tags'] = str(y['tags'])

                    cursor.execute(sql, y)
                    conn.commit()
                    pbar.set_description(y['title'] + '已导入')
                except:
                    pbar.set_description(y['title'] + '已存在')







if __name__ == '__main__':


    city = '上海'
    #SaveCityBorderIntoDB(city)  # 下载城市区域数据
    #HoleCityDown(city)  # 下载区域住房数据
    GetCompleteHousingInfo('上海')#获取详细在售房屋
