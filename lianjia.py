import execjs
import requests
import time
import set
import json
import sqlite3
import numpy

current_milli_time = lambda: int(round(time.time() * 1000))
def get_js():
    f = open("authorization.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr



def requlianjia(
        max_lat=31.291756,
        min_lat=31.283656,
        max_lng=121.546738,
        min_lng=121.536731,
        group_type='community'
):
    ###########-----计算authorization值-----############
    time_13 = current_milli_time()
    city_id = 310000
    jsstr = get_js()
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
            return house_json['data']['list']
        else:
            return None
def SaveCityBorderIntoDB():#读取上海市各个区域轮廓
    ret = requlianjia(max_lat=31.337967, min_lat=31.078528, max_lng=121.573176, min_lng=121.252948,
                      group_type='district')
    conn = sqlite3.connect('LianJia.db')#链接数据库
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
                    )''' % 'sh310000'
        cursor.execute(sql)
    except:
        print('数据表已存在')
    for x in ret:
        try:
            sql = ''' insert into sh310000
                              (id, name, longitude,latitude,border,unit_price,count)
                              values
                              (:id, :name, :longitude, :latitude, :border, :unit_price, :count)'''
            cursor.execute(sql, ret[x])
            conn.commit()
            print(ret[x]['name'], '已导入')
        except:
            print(ret[x]['name'], '地区已存在')

    cursor.close()
    # for x in numpy.arange(121.118774, 121.944122, 0.1):
    #     for y in numpy.arange(30.820294, 31.487821, 0.1):
    #         print((round(y,6), round(y - 0.1,6), round(x,6), round(x - 0.1,6)))
    #         print(requlianjia(round(y,6), round(y - 0.1,6), round(x,6), round(x - 0.1,6)))
def HoleCityDown():
    conn = sqlite3.connect('LianJia.db')
    c = conn.cursor()
    c.execute('SELECT * FROM sh310000')
    area_list = c.fetchall()
    lat = []
    lng = []
    conn = sqlite3.connect('LianJia.db')
    cursor = conn.cursor()

    for x in area_list:
        for y in x[4].split(';'):
            lng.append(float(y.split(',')[0]))
            lat.append(float(y.split(',')[1]))

        try:
            sql = '''create table %s (
                            id int PRIMARY KEY ,
                            name text,
                            longitude text,
                            latitude text,
                            unit_price int,
                            count int
                            )''' % 'house'
            cursor.execute(sql)
            '''使用游标关闭数据库的链接'''
        except:
            print('数据表已存在')
        for x in numpy.arange(min(lng), max(lng), 0.01):
            for y in numpy.arange(min(lat), max(lat), 0.01):
                # print((round(y, 6), round(y - 0.01, 6), round(x, 6), round(x - 0.01, 6)))
                ret = requlianjia(round(y, 6), round(y - 0.01, 6), round(x, 6), round(x - 0.01, 6))
                if ret is not None:
                    for z in ret:
                        if type(z) is not dict:
                            for r in z:
                                print(ret[z])
                                try:
                                    sql = ''' insert into house
                                                          (id, name, longitude,latitude,unit_price,count)
                                                          values
                                                          (:id, :name, :longitude, :latitude, :unit_price, :count)'''
                                    cursor.execute(sql, ret[z])
                                    conn.commit()
                                    print(ret[z]['name'], '已导入')
                                except:
                                    print(ret[z]['name'], '住房已存在')

                        else:
                            print(z)
                            try:
                                sql = ''' insert into house
                                                      (id, name, longitude,latitude,unit_price,count)
                                                      values
                                                      (:id, :name, :longitude, :latitude, :unit_price, :count)'''
                                cursor.execute(sql, z)
                                conn.commit()
                                print(z['name'], '已导入')
                            except:
                                print(z['name'], '住房已存在')

if __name__ == '__main__':
    SaveCityBorderIntoDB()#下载城市区域数据
    HoleCityDown()#下载区域住房数据







