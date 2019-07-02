import requests
import time
import tqdm
import json
import sqlite3
import numpy
import math
import hashlib

sql_InsertDetailInfo = '''insert into %s(houseId,houseCode,title,appid,source,imgSrc,layoutImgSrc,imgSrcUri,layoutImgSrcUri,roomNum,square,buildingArea,buildYear,isNew,ctime,mtime,orientation,floorStat,totalFloor,decorateType,hbtName,isYezhuComment,isGarage,houseType,isFocus,status,isValid,signTime,signSource,signSourceCn,isDisplay,address,community,communityId,communityName,communityUrl,communityUrlEsf,districtId,districtUrl,districtName,regionId,regionUrl,regionName,bbdName,bbdUrl,houseCityId,subwayInfo,schoolName,schoolArr,bizcircleFullSpell,house_video_info,price,unitPrice,viewUrl,listPrice,publishTime,isVilla,villaNoFloorLevel,villaName,tags)values(:houseId,:houseCode,:title,:appid,:source,:imgSrc,:layoutImgSrc,:imgSrcUri,:layoutImgSrcUri,:roomNum,:square,:buildingArea,:buildYear,:isNew,:ctime,:mtime,:orientation,:floorStat,:totalFloor,:decorateType,:hbtName,:isYezhuComment,:isGarage,:houseType,:isFocus,:status,:isValid,:signTime,:signSource,:signSourceCn,:isDisplay,:address,:community,:communityId,:communityName,:communityUrl,:communityUrlEsf,:districtId,:districtUrl,:districtName,:regionId,:regionUrl,:regionName,:bbdName,:bbdUrl,:houseCityId,:subwayInfo,:schoolName,:schoolArr,:bizcircleFullSpell,:house_video_info,:price,:unitPrice,:viewUrl,:listPrice,:publishTime,:isVilla,:villaNoFloorLevel,:villaName,:tags)'''
sql_CreateDetailInfo = '''create table %s (houseId PRIMARY  KEY 
            , houseCode, title, appid, source, imgSrc, layoutImgSrc, imgSrcUri,
            layoutImgSrcUri, roomNum, square, buildingArea, buildYear, isNew, ctime,
            mtime, orientation, floorStat, totalFloor, decorateType, hbtName,
            isYezhuComment, isGarage, houseType, isFocus, status, isValid, signTime,
            signSource, signSourceCn, isDisplay, address, community, communityId,
            communityName, communityUrl, communityUrlEsf, districtId, districtUrl,
            districtName, regionId, regionUrl, regionName, bbdName, bbdUrl, houseCityId,
            subwayInfo, schoolName, schoolArr, bizcircleFullSpell, house_video_info , price,
            unitPrice, viewUrl, listPrice, publishTime, isVilla, villaNoFloorLevel,
            villaName, tags)'''
class Lianjia():
    def __init__(self, city):
        self.city_dict = {
            '上海': {'city_id': '310000', 'max_lat': '31.36552', 'min_lat': '31.106158', 'max_lng': '121.600985',
                   'min_lng': '121.360095'},
            '北京': {'city_id': '110000', 'max_lat': '40.074766', 'min_lat': '39.609408', 'max_lng': '116.796856',
                   'min_lng': '115.980476'},
            '广州': {'city_id': '440100', 'max_lat': '23.296086', 'min_lat': '22.737277', 'max_lng': '113.773905',
                   'min_lng': '113.038013'},
            '深圳': {'city_id': '440300', 'max_lat': '22.935891', 'min_lat': '22.375581', 'max_lng': '114.533683',
                   'min_lng': '113.797791'},
            '长沙': {'city_id': '430100', 'max_lat': '28.368467', 'min_lat': '28.101143', 'max_lng': '113.155889',
                   'min_lng': '112.735051'},
            '烟台': {'city_id': '370600', 'max_lat': '37.590234', 'min_lat': '37.349651', 'max_lng': '121.698469',
                   'min_lng': '121.210365'},
            '厦门': {'city_id': '350200', 'max_lat': '24.794145', 'min_lat': '24.241819', 'max_lng': '118.533083',
                   'min_lng': '117.892627'},
            '郑州':{'city_id': '410100', 'max_lat': '34.961967', 'min_lat': '34.473941', 'max_lng': '113.50206',
                   'min_lng': '112.899549'}
        }
        #https://ajax.lianjia.com/map/search/ershoufang/?callback=jQuery111109719454800982295_1562045315950&city_id=410100&group_type=district&max_lat=34.961967&min_lat=34.473941&max_lng=113.50206&min_lng=112.899549&sug_id=&sug_type=&filters=%7B%7D&request_ts=1562045339940&source=ljpc&authorization=a83c1b0e615c19505b0a399051fcb87f&_=1562045315957

        self.city_id = self.city_dict[city]['city_id']
        self.city = city
        self.url_fang = 'https://ajax.lianjia.com/map/resblock/ershoufanglist/?callback=jQuery11110617424919783834_1541868368031' \
                        '&id=%s' \
                        '&order=0' \
                        '&page=%d' \
                        '&filters=%s' \
                        '&request_ts=%d' \
                        '&source=ljpc' \
                        '&authorization=%s' \
                        '&_=%d'
        self.url = 'https://ajax.lianjia.com/map/search/ershoufang/?callback=jQuery1111012389114747347363_1534230881479' \
                   '&city_id=%s' \
                   '&group_type=%s' \
                   '&max_lat=%s' \
                   '&min_lat=%s' \
                   '&max_lng=%s' \
                   '&min_lng=%s' \
                   '&filters=%s' \
                   '&request_ts=%d' \
                   '&source=ljpc' \
                   '&authorization=%s' \
                   '&_=%d'
        self.cookies = {'lianjia_uuid': '9bdccc1a-7584-4639-ba95-b42cf21bbbc7',
                        'jzqa': '1.3180246719396510700.1534145942.1534145942.1534145942.1',
                        'jzqckmp': '1',
                        'ga': 'GA1.2.964691746.1534145946',
                        'gid': 'GA1.2.826685830.1534145946',
                        'UM_distinctid': '165327625186a-029cf60b1994ee-3461790f-fa000-165327625199d3',
                        'select_city': '310000',
                        'lianjia_ssid': '34fc4efa-7fcc-4f3f-82ae-010401f27aa8',
                        '_smt_uid': '5b72c5f7.5815bcdf',
                        'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1537530243',
                        'select_city': '110000',
                        '_jzqc': '1',
                        '_gid': 'GA1.2.178601063.1541866763',
                        '_jzqb': '1.2.10.1541866760.1'

                        }
        # '''
        # select_city=110000;
        # _jzqa=1.3180246719396510700.1534145942.1537530221.1541866760.3;
        # _jzqc=1;
        # _jzqckmp=1;
        # _gid=GA1.2.178601063.1541866763;
        # _jzqb=1.2.10.1541866760.1'''
        self.headers = {
            'Host': 'ajax.lianjia.com',
            'Referer': 'https://sh.lianjia.com/ditu/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

    def GetMD5(self, string_):
        m = hashlib.md5()
        m.update(string_.encode('utf-8'))
        return m.hexdigest()

    def GetAuthorization(self, dict_) -> str:
        datastr = "vfkpbin1ix2rb88gfjebs0f60cbvhedlcity_id={city_id}group_type={group_type}max_lat={max_lat}" \
                  "max_lng={max_lng}min_lat={min_lat}min_lng={min_lng}request_ts={request_ts}".format(
            city_id=dict_["city_id"],
            group_type=dict_["group_type"],
            max_lat=dict_["max_lat"],
            max_lng=dict_["max_lng"],
            min_lat=dict_["min_lat"],
            min_lng=dict_["min_lng"],
            request_ts=dict_["request_ts"])
        authorization = self.GetMD5(datastr)
        return authorization

    def GetDistrictInfo(self) -> list:
        """
        :str max_lat:
        最大经度 六位小数str型max_lat='40.074766'

        :str min_lat:
        最小经度 六位小数str型min_lat='39.609408'

        :str max_lng:
        最大纬度 六位小数str型max_lng='40.074766'

        :str min_lng:
        最小纬度 六位小数str型min_lng='39.609408'

        :str city_id:
        北京:110000  上海:310000

        #获取上海的各个区域，例如浦东，长宁，徐汇

        :return: list

        [{'id': 310115, 'name': '浦东', 'longitude': 121.60653130552, 'latitude': 31.208001618509, 'border': '121.54148868942,31.347913060234', 'unit_price': 58193, 'count': 18866},
        {'id': 310112, 'name': '闵行', 'longitude': 121.40817118429, 'latitude': 31.091185835136, 'border': '121.34040533465,31.037672798655;121.34022400061,31.022622576909;121.33932297393,31.020472421859;121.35006370183,31.020640362869', 'unit_price': 51866, 'count': 9024},
        {'id': 310113, 'name': '宝山', 'longitude': 121.42883034102, 'latitude': 31.369477510376, 'border': '121.37795619808,','unit_price': 18486, 'count': 76}]
        .........

        """

        time_13 = int(round(time.time() * 1000))
        authorization = Lianjia(self.city).GetAuthorization(
            {'group_type': 'district', 'city_id': self.city_id, 'max_lat': self.city_dict[self.city]['max_lat'],
             'min_lat': self.city_dict[self.city]['min_lat'],
             'max_lng': self.city_dict[self.city]['max_lng'], 'min_lng': self.city_dict[self.city]['min_lng'],
             'request_ts': time_13})

        url = self.url % (
            self.city_id, 'district', self.city_dict[self.city]['max_lat'], self.city_dict[self.city]['min_lat'],
            self.city_dict[self.city]['max_lng'], self.city_dict[self.city]['min_lng'], '%7B%7D', time_13,
            authorization, time_13)

        with requests.Session() as sess:
            ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)

            house_json = json.loads(ret.text[43:-1])

            if house_json['errno'] == 0:

                return house_json['data']['list'].values()

            else:
                return None

    def GetCommunityInfo(self, max_lat, min_lat, max_lng, min_lng) -> list:

        """
        :str max_lat:
        最大经度 六位小数str型max_lat='40.074766'

        :str min_lat:
        最小经度 六位小数str型min_lat='39.609408'

        :str max_lng:
        最大纬度 六位小数str型max_lng='40.074766'

        :str min_lng:
        最小纬度 六位小数str型min_lng='39.609408'

        :str city_id:
        北京:110000  上海:310000


        #获取区域内在售小区的信息#例如上海市的陈湾小区ID地理位置平均价格在售套数

        :return: list

        [{'id': '5011000012693', 'name': '陈湾小区', 'longitude': 121.455211, 'latitude': 30.966981, 'unit_price': 24407, 'count': 9}]


        """

        time_13 = int(round(time.time() * 1000))
        authorization = Lianjia(self.city).GetAuthorization(
            {'group_type': 'community', 'city_id': self.city_id, 'max_lat': max_lat, 'min_lat': min_lat,
             'max_lng': max_lng, 'min_lng': min_lng, 'request_ts': time_13})

        url = self.url % (
            self.city_id, 'community', max_lat, min_lat, max_lng, min_lng, '%7B%7D', time_13, authorization, time_13)

        with requests.Session() as sess:
            ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)
            house_json = json.loads(ret.text[43:-1])

            if house_json['errno'] == 0:
                data_list = []
                if type(house_json['data']['list']) is dict:
                    for x in house_json['data']['list']:
                        data_list.append(house_json['data']['list'][x])
                    return data_list
                else:
                    return house_json['data']['list']

            else:
                return None

    def GetHousingInfo(self, id, count) -> list:

        ll = []
        for page in range(1, math.ceil(count / 10) + 1):
            time_13 = int(round(time.time() * 1000))
            authorization = self.GetMD5(
                "vfkpbin1ix2rb88gfjebs0f60cbvhedlid={id}order={order}page={page}request_ts={request_ts}".format(
                    id=id, order=0, page=1, request_ts=time_13))
            # e = {id: "1111027380242", order: 0, page: 1, filters: "{}", request_ts: 1541871468249} 1b9f64bd353667b4e44ed593eca6451d
            ###############-----拼接请求url-----#################
            url = self.url_fang % (id, page, '%7B%7D', time_13, authorization, time_13)
            with requests.Session() as sess:
                ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)

                house_json = json.loads(ret.text[41:-1])

                try:
                    for x in house_json['data']['ershoufang_info']['list']:
                        ll.append(house_json['data']['ershoufang_info']['list'][x])
                except:
                    print(house_json)

        return ll


def SaveCityBorderIntoDB(city):  # 读取某市各个区域轮廓
    ret = Lianjia(city).GetDistrictInfo()
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
        sql = ''' 
            insert into %s
            (id, name, longitude,latitude,border,unit_price,count)
            values
            (:id, :name, :longitude, :latitude, :border, :unit_price, :count)
            ''' % city
        try:
            cursor.execute(sql, x)
            conn.commit()
            pbar.set_description(x['name'] + '已导入')
        except:
            pbar.set_description(x['name'] + '已存在')

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
        pass
    for x in area_list:
        lat = []
        lng = []
        district = x[1]
        for y in x[0].split(';'):
            lng.append(float(y.split(',')[0]))
            lat.append(float(y.split(',')[1]))
        li = []
        step = 0.02
        for x in numpy.arange(min(lng), max(lng), step):
            for y in numpy.arange(min(lat), max(lat), step):
                li.append((round(y, 6), round(y - step, 6), round(x, 6), round(x - step, 6)))
        pbar = tqdm.tqdm(li)
        for x in pbar:

            ret = Lianjia(city).GetCommunityInfo(x[0], x[1], x[2], x[3])

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

                        pbar.set_description(district + z['name'] + '已导入')
                    except:

                        pbar.set_description(district + z['name'] + '住房已存在')


def GetCompleteHousingInfo(city):
    # 爬取所有小区内每个住房信息
    with sqlite3.connect('DetailInfo.db') as conn1:
        cursor1 = conn1.cursor()
        try:
            sql = sql_CreateDetailInfo % city
            cursor1.execute(sql)
        except:
            pass

    with sqlite3.connect('LianJia_area.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id,count FROM %s' % city)
        area_list = c.fetchall()
    pbar = tqdm.tqdm(area_list)
    for x in pbar:
        ret = Lianjia(city).GetHousingInfo(x[0], x[1])
        with sqlite3.connect('DetailInfo.db') as conn:
            cursor = conn.cursor()
            for y in ret:
                try:
                    sql = sql_InsertDetailInfo % city
                    y['house_video_info'] = str(y['house_video_info'])
                    y['tags'] = str(y['tags'])
                    cursor.execute(sql, y)
                    conn.commit()
                    pbar.set_description(y['title'] + '已导入')
                except:
                    pbar.set_description(y['title'] + '已存在')


if __name__ == '__main__':
    city = '郑州'
    #SaveCityBorderIntoDB(city)  # 下载城市区域数据
    HoleCityDown(city)  # 下载区域住房数据
    #GetCompleteHousingInfo(city)  # 获取详细在售房屋
