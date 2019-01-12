import requests
from testing import *
from lxml import etree
url_img = "http://210.40.2.253:8888/CheckCode.aspx?"
url_login = "http://210.40.2.253:8888/default2.aspx"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
}


def login():
    s = requests.session()
    response = s.get(url_login)
    selector = etree.HTML(response.content)
    __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]  # 获取__VIEWSTATE
    count = 0
    sum = 0
    for i in range(100):
        response = s.get(url_img, stream=True)
        image = response.content
        with open('c.jpg', "wb") as img:
            img.write(image)
        txtSecretCode = crack_captcha()
        data = {
            '__VIEWSTATE': __VIEWSTATE,
            'TextBox2': '123',
            'txtSecretCode': txtSecretCode,
            'txtUserName': '1600',
            "button1": ''
        }
        response = s.post(url_login, headers=header, data=data)
        s1 = response.content.decode('gb2312')  # 转码，
        sum += 1
        if s1.find('验证码不正确') != -1:
            with open('F/' + txtSecretCode + '.jpg', "wb") as img:
                img.write(image)

        else:
            with open('T/' + txtSecretCode + '.jpg', "wb") as img:
                img.write(image)
            count += 1

        img.close()
    print(count/sum)

login()
