city = {'长沙': {'city_id': '430100', 'max_lat': '28.368467', 'min_lat': '28.101143', 'max_lng': '113.155889',
               'min_lng': '112.735051'},
        '上海': {'city_id': '310000', 'max_lat': '31.36552', 'min_lat': '31.106158', 'max_lng': '121.600985',
               'min_lng': '121.360095'},
        '北京': {'city_id': '110000', 'max_lat': '40.074766', 'min_lat': '39.609408', 'max_lng': '116.796856',
               'min_lng': '115.980476'}
        }

url_fang='''https://ajax.lianjia.com/map/resblock/ershoufanglist/?callback=jQuery111106822012072868358_1534402288206&id=%s&order=0&page=%d&filters=%s&request_ts=%d&source=ljpc&authorization=%s&_=%d'''#%7B%7D

url = 'https://ajax.lianjia.com/map/search/ershoufang/?callback=jQuery1111012389114747347363_1534230881479' \
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
cookies = {'lianjia_uuid': '9bdccc1a-7584-4639-ba95-b42cf21bbbc7',
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
headers = {
'Host': 'ajax.lianjia.com',
'Referer': 'https://bj.lianjia.com/ditu/',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
js = '''
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
