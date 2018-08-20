import execjs
import requests
import time
import tqdm
import json
import sqlite3
import numpy
import math

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
            '长沙': {'city_id': '430100', 'max_lat': '28.368467', 'min_lat': '28.101143', 'max_lng': '113.155889',
                   'min_lng': '112.735051'},
            '上海': {'city_id': '310000', 'max_lat': '31.36552', 'min_lat': '31.106158', 'max_lng': '121.600985',
                   'min_lng': '121.360095'},
            '北京': {'city_id': '110000', 'max_lat': '40.074766', 'min_lat': '39.609408', 'max_lng': '116.796856',
                   'min_lng': '115.980476'},
            '烟台': {'city_id': '370600', 'max_lat': '37.590234', 'min_lat': '37.349651', 'max_lng': '121.698469',
                   'min_lng': '121.210365'},
            '厦门': {'city_id': '350200', 'max_lat': '24.794145', 'min_lat': '24.241819', 'max_lng': '118.533083',
                   'min_lng': '117.892627'}
            }
        self.city_id = self.city_dict[city]['city_id']
        self.city=city

        self.url_fang = '''https://ajax.lianjia.com/map/resblock/ershoufanglist/?callback=jQuery111106822012072868358_1534402288206&id=%s&order=0&page=%d&filters=%s&request_ts=%d&source=ljpc&authorization=%s&_=%d'''
        # %7B%7D
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
                   'gat': '1',
                   'gat_past': '1',
                   'gat_global': '1',
                   'gat_new_global': '1',
                   'gat_dianpu_agent': '1'
                   }
        self.headers = {
            'Host': 'ajax.lianjia.com',
            'Referer': 'https://bj.lianjia.com/ditu/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.js = '''
        var window = window || {};

        function e(e, t) {
            var n = (65535 & e) + (65535 & t);
            return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
        }

        function t(e, t) {
            return e << t | e >>> 32 - t
        }

        function n(n, i, a, r, o, s) {
            return e(t(e(e(i, n), e(r, s)), o), a)
        }

        function i(e, t, i, a, r, o, s) {
            return n(t & i | ~t & a, e, t, r, o, s)
        }

        function a(e, t, i, a, r, o, s) {
            return n(t & a | i & ~a, e, t, r, o, s)
        }

        function r(e, t, i, a, r, o, s) {
            return n(t ^ i ^ a, e, t, r, o, s)
        }

        function o(e, t, i, a, r, o, s) {
            return n(i ^ (t | ~a), e, t, r, o, s)
        }

        function s(t, n) {
            t[n >> 5] |= 128 << n % 32,
                t[14 + (n + 64 >>> 9 << 4)] = n;
            var s, l, c, d, u, g = 1732584193,
                f = -271733879,
                m = -1732584194,
                p = 271733878;
            for (s = 0; s < t.length; s += 16) l = g,
                c = f,
                d = m,
                u = p,
                g = i(g, f, m, p, t[s], 7, -680876936),
                p = i(p, g, f, m, t[s + 1], 12, -389564586),
                m = i(m, p, g, f, t[s + 2], 17, 606105819),
                f = i(f, m, p, g, t[s + 3], 22, -1044525330),
                g = i(g, f, m, p, t[s + 4], 7, -176418897),
                p = i(p, g, f, m, t[s + 5], 12, 1200080426),
                m = i(m, p, g, f, t[s + 6], 17, -1473231341),
                f = i(f, m, p, g, t[s + 7], 22, -45705983),
                g = i(g, f, m, p, t[s + 8], 7, 1770035416),
                p = i(p, g, f, m, t[s + 9], 12, -1958414417),
                m = i(m, p, g, f, t[s + 10], 17, -42063),
                f = i(f, m, p, g, t[s + 11], 22, -1990404162),
                g = i(g, f, m, p, t[s + 12], 7, 1804603682),
                p = i(p, g, f, m, t[s + 13], 12, -40341101),
                m = i(m, p, g, f, t[s + 14], 17, -1502002290),
                f = i(f, m, p, g, t[s + 15], 22, 1236535329),
                g = a(g, f, m, p, t[s + 1], 5, -165796510),
                p = a(p, g, f, m, t[s + 6], 9, -1069501632),
                m = a(m, p, g, f, t[s + 11], 14, 643717713),
                f = a(f, m, p, g, t[s], 20, -373897302),
                g = a(g, f, m, p, t[s + 5], 5, -701558691),
                p = a(p, g, f, m, t[s + 10], 9, 38016083),
                m = a(m, p, g, f, t[s + 15], 14, -660478335),
                f = a(f, m, p, g, t[s + 4], 20, -405537848),
                g = a(g, f, m, p, t[s + 9], 5, 568446438),
                p = a(p, g, f, m, t[s + 14], 9, -1019803690),
                m = a(m, p, g, f, t[s + 3], 14, -187363961),
                f = a(f, m, p, g, t[s + 8], 20, 1163531501),
                g = a(g, f, m, p, t[s + 13], 5, -1444681467),
                p = a(p, g, f, m, t[s + 2], 9, -51403784),
                m = a(m, p, g, f, t[s + 7], 14, 1735328473),
                f = a(f, m, p, g, t[s + 12], 20, -1926607734),
                g = r(g, f, m, p, t[s + 5], 4, -378558),
                p = r(p, g, f, m, t[s + 8], 11, -2022574463),
                m = r(m, p, g, f, t[s + 11], 16, 1839030562),
                f = r(f, m, p, g, t[s + 14], 23, -35309556),
                g = r(g, f, m, p, t[s + 1], 4, -1530992060),
                p = r(p, g, f, m, t[s + 4], 11, 1272893353),
                m = r(m, p, g, f, t[s + 7], 16, -155497632),
                f = r(f, m, p, g, t[s + 10], 23, -1094730640),
                g = r(g, f, m, p, t[s + 13], 4, 681279174),
                p = r(p, g, f, m, t[s], 11, -358537222),
                m = r(m, p, g, f, t[s + 3], 16, -722521979),
                f = r(f, m, p, g, t[s + 6], 23, 76029189),
                g = r(g, f, m, p, t[s + 9], 4, -640364487),
                p = r(p, g, f, m, t[s + 12], 11, -421815835),
                m = r(m, p, g, f, t[s + 15], 16, 530742520),
                f = r(f, m, p, g, t[s + 2], 23, -995338651),
                g = o(g, f, m, p, t[s], 6, -198630844),
                p = o(p, g, f, m, t[s + 7], 10, 1126891415),
                m = o(m, p, g, f, t[s + 14], 15, -1416354905),
                f = o(f, m, p, g, t[s + 5], 21, -57434055),
                g = o(g, f, m, p, t[s + 12], 6, 1700485571),
                p = o(p, g, f, m, t[s + 3], 10, -1894986606),
                m = o(m, p, g, f, t[s + 10], 15, -1051523),
                f = o(f, m, p, g, t[s + 1], 21, -2054922799),
                g = o(g, f, m, p, t[s + 8], 6, 1873313359),
                p = o(p, g, f, m, t[s + 15], 10, -30611744),
                m = o(m, p, g, f, t[s + 6], 15, -1560198380),
                f = o(f, m, p, g, t[s + 13], 21, 1309151649),
                g = o(g, f, m, p, t[s + 4], 6, -145523070),
                p = o(p, g, f, m, t[s + 11], 10, -1120210379),
                m = o(m, p, g, f, t[s + 2], 15, 718787259),
                f = o(f, m, p, g, t[s + 9], 21, -343485551),
                g = e(g, l),
                f = e(f, c),
                m = e(m, d),
                p = e(p, u);
            return [g, f, m, p]
        }

        function l(e) {
            var t, n = "";
            for (t = 0; t < 32 * e.length; t += 8) n += String.fromCharCode(e[t >> 5] >>> t % 32 & 255);
            return n
        }

        function c(e) {
            var t, n = [];
            for (n[(e.length >> 2) - 1] = void 0, t = 0; t < n.length; t += 1) n[t] = 0;
            for (t = 0; t < 8 * e.length; t += 8) n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
            return n
        }

        function d(e) {
            return l(s(c(e), 8 * e.length))
        }

        function u(e, t) {
            var n, i, a = c(e),
                r = [],
                o = [];
            for (r[15] = o[15] = void 0, a.length > 16 && (a = s(a, 8 * e.length)), n = 0; n < 16; n += 1) r[n] = 909522486 ^ a[n],
                o[n] = 1549556828 ^ a[n];
            return i = s(r.concat(c(t)), 512 + 8 * t.length),
                l(s(o.concat(i), 640))
        }

        function g(e) {
            var t, n, i = "0123456789abcdef",
                a = "";
            for (n = 0; n < e.length; n += 1) t = e.charCodeAt(n),
                a += i.charAt(t >>> 4 & 15) + i.charAt(15 & t);
            return a
        }

        function f(e) {
            return unescape(encodeURIComponent(e))
        }

        function m(e) {
            return d(f(e))
        }

        function p(e) {
            return g(m(e))
        }

        function _(e, t) {
            return u(f(e), f(t))
        }

        function h(e, t) {
            return g(_(e, t))
        }

        function v(e, t, n) {
            return t ? n ? _(t, e) : h(t, e) : n ? m(e) : p(e)
        }

        function getMd5(e) {
            var t = [],
                i = "";
            for (var a in e) t.push(a);
            t.sort();
            for (var a = 0; a < t.length; a++) {
                var r = t[a];
                "filters" !== r && (i += r + "=" + e[r])
            }
            return i ? (window.md5 = n, v("vfkpbin1ix2rb88gfjebs0f60cbvhedl" + i)) : "";
        }
        '''


    def GetAuthorization(self, dict)->str:
        jsstr = self.js
        ctx = execjs.compile(jsstr)
        authorization = ctx.call('getMd5', dict)
        return authorization

    def GetDistrictInfo(self)->list:
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
            {'group_type': 'district', 'city_id': self.city_id, 'max_lat': self.city_dict[self.city]['max_lat'], 'min_lat': self.city_dict[self.city]['min_lat'],
             'max_lng': self.city_dict[self.city]['max_lng'], 'min_lng': self.city_dict[self.city]['min_lng'], 'request_ts': time_13})

        url = self.url % (
            self.city_id, 'district', self.city_dict[self.city]['max_lat'], self.city_dict[self.city]['min_lat'], self.city_dict[self.city]['max_lng'], self.city_dict[self.city]['min_lng'], '%7B%7D', time_13, authorization, time_13)

        with requests.Session() as sess:
            ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)

            house_json = json.loads(ret.text[43:-1])

            if house_json['errno'] == 0:

                return house_json['data']['list'].values()

            else:
                return None

    def GetCommunityInfo(self,max_lat, min_lat, max_lng, min_lng)->list:

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

    def GetHousingInfo(self,id, count)->list:

        ll = []
        for page in range(1, math.ceil(count / 10) + 1):
            time_13 = int(round(time.time() * 1000))
            jsstr = self.js
            ctx = execjs.compile(jsstr)
            authorization = ctx.call('getMd5',
                                     {'filters': "{}", 'id': id, 'order': 0, 'page': page, 'request_ts': time_13})
            ###############-----拼接请求url-----#################
            url = self.url_fang % (id, page, '%7B%7D', time_13, authorization, time_13)

            with requests.Session() as sess:
                ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)
                house_json = json.loads(ret.text[42:-1])

                for x in house_json['data']['ershoufang_info']['list']:
                    ll.append(house_json['data']['ershoufang_info']['list'][x])

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
        pass
    for x in area_list:
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
    city = '北京'
    #SaveCityBorderIntoDB(city)  # 下载城市区域数据
    #HoleCityDown(city)  # 下载区域住房数据
    GetCompleteHousingInfo(city)#获取详细在售房屋
