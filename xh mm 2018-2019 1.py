from requests import session
from sys import argv
from testing import *
from lxml import etree

xhmm = os.path.basename(argv[0]).split(".")[0].split()
xh = ''
mm = ''
ddlXN = ''
ddlXQ = ''
try:
    xh = xhmm[0]
    mm = xhmm[1]
    ddlXN = xhmm[2]
    ddlXQ = xhmm[3]
except IndexError:
    print('文件命名格式：学号 密码 学年 学期')

url_login = "http://210.40.2.253:8888/default2.aspx"
url_img = "http://210.40.2.253:8888/CheckCode.aspx?"
url_score = 'http://210.40.2.253:8888/xscj_gc.aspx?xh=' + xh + '&gnmkdm=N121605'
header = {
    'Referer': url_login + 'xs_main.aspx?xh=' + xh,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
}
filename = 'c.jpg'


def login():
    s = session()
    response = s.get(url_login)
    selector = etree.HTML(response.content)
    __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]  # 获取__VIEWSTATE
    count = 0
    sum = 0
    print('连接中')
    while True:
        response = s.get(url_img, stream=True)
        image = response.content
        with open(filename, "wb") as img:
            img.write(image)

        print('验证码', end='')
        txtSecretCode = crack_captcha()
        print(txtSecretCode)
        data = {
            '__VIEWSTATE': __VIEWSTATE,
            'TextBox2': mm,
            'txtSecretCode': txtSecretCode,
            'txtUserName': xh,
            "button1": ''
        }
        response = s.post(url_login, headers=header, data=data)
        s1 = response.content.decode('gb2312')  # 转码，
        sum += 1
        if s1.find('欢迎您') != -1:
            return s


def get_score(s):
    response = s.get(url_score, headers=header)  # 获取__VIEWSTATE
    selector = etree.HTML(response.content)
    __VIEWSTATE = selector.xpath('//*[@id="Form1"]/input/@value')[0]

    data = {
        '__VIEWSTATE': __VIEWSTATE,
        'Button1': '%B0%B4%D1%A7%C6%DA%B2%E9%D1%AF',
        'ddlXN': ddlXN,
        'ddlXQ': ddlXQ,
    }
    response = s.post(url_score, headers=header, data=data)
    s.close()
    str = response.content.decode('gb2312')
    selector = etree.HTML(str)
    content = selector.xpath('//table[@id="Datagrid1"]/tr/td/text()')
    return content


def str2num(str):
    if str == '优秀':
        return 90
    if str == '良好':
        return 80
    if str == '中等':
        return 70
    if str == '及格':
        return 60
    return float(str)


def get_info(content):
    i = 16
    sum_cj = 0
    sum_xf = 0
    sum_jd = 0
    while i < len(content):
        xn = content[i]
        xq = content[i + 1]
        kcdm = content[i + 2]
        kcmc = content[i + 3]
        kcxz = content[i + 4]
        xf = float(content[i + 6])
        jd = float(content[i + 7].strip())
        cj = content[i + 8]
        print('%s %s %-10s %s\t%.1f %.1f %s %s' % (xn, xq, kcdm, cj, xf, jd, kcmc, kcxz))
        sum_xf += xf
        sum_cj += xf * str2num(cj)
        sum_jd += xf * jd
        i += 15
    print('%.3f %.3f' % (sum_cj / sum_xf, sum_jd / sum_xf))


def main():
    s = login()
    content = get_score(s)
    get_info(content)
    input('@jjccero')


try:
    main()
except:
    input('似乎哪里有错')
