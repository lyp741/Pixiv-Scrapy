#! usr/bin/python
#coding=utf-8 
import urllib
import urllib2
import re
import os
import threading
import cookielib


pixiv_id = 'username'  #用户p站id或者邮箱
password = 'password'  #用户密码

member_id = '6996493'  #画师ID
pages = 16  #作品页数

save_path = "~/Desktop/Mavis/"  #保存路径

cookie = cookielib.MozillaCookieJar('cookie.txt')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
def login():
    request = urllib2.Request("https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index")
    response = opener.open(request)
    content = response.read()
    pattern = re.compile('''"pixivAccount.postKey":"(.*?)"''')
    items = re.findall(pattern, content)
    print items



    header = {
        "Accept-Language": "zh-CN,zh;q=0.8",
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }
    loginInfo = urllib.urlencode({
        'password': password,
        'pixiv_id': pixiv_id,
        'post_key':items[0],
        'captcha':'',
        'g_recaptcha_response':'',
        'source':'pc',
        'ref':'wwwtop_accounts_index',
        'return_to':'http://www.pixiv.net/'
    })

    loginUrl = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
    request = urllib2.Request(loginUrl, data=loginInfo, headers=header)
    opener.open(request).read()
    cookie.save(ignore_discard = True, ignore_expires = True)
    #opener.open("http://www.pixiv.net/member_illust.php?id=7210261&p=7").read()


basesite = "http://www.pixiv.net/member_illust.php?id=" + member_id
##http://www.pixiv.net/member_illust.php?id=7210261&p=2

index = 0
def getImages(content):
    #pattern = re.compile('''<img.*?src="http://imgsrc.baidu.com/forum/.*?/sign=.*?/(.*?)" ''')
    pattern = re.compile('''img/(.*?)_master1200.(.*?)"''')
    items = re.findall(pattern, content)
    contents = []
    for item in items:
        contents.append(item)
    return contents

def getPage(x):
    url = "%s%d" % (basesite+"&p=" , x)
    request = urllib2.Request(url)
    print url
    response = opener.open(request)
    return response.read()


def saveImgs(images):
    number = 1
    print  len(images)
    try:
        os.mkdir(os.path.expanduser(save_path))
    except OSError , e:
        print "Existed"
    global index
    threads = []
    for imageURL in images:
        index = index + 1
        fileName = os.path.expanduser(save_path) + "%d."%index+imageURL[1]
        #saveImg(imageURL, fileName)
        thread = threading.Thread(target=saveImg,args=(imageURL,fileName))
        thread.start()
        threads.append(thread) 
    for i in threads:
        i.join()



def saveImg(imageURL, fileName):
    #u = urllib.urlopen(imageURL)
    #data = u.read()
    #imageURL = 2016/07/24/00/03/10/58055191_p0
    imgurl = '''http://i3.pixiv.net/img-original/img/'''
    pattern = re.compile('''.*?/.*?/.*?/.*?/.*?/.*?/(.*?)_p0''')
    items = re.findall(pattern, imageURL[0])
    illust_id = items[0]
    uurrll = imgurl + imageURL[0] + "." + imageURL[1]
    request = urllib2.Request(uurrll)
    referer = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + illust_id
    request.add_header('Referer', referer)
    request.add_header('User-Agent',"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8")
    try:
        response = opener.open(request)
        data = response.read()
        f = open(fileName, 'wb')
        f.write(data)
        print  fileName + "succeed"
        f.close()
    except Exception,e:
        uurrll = imgurl + imageURL[0] + ".png" 
        request = urllib2.Request(uurrll)
        referer = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + illust_id
        request.add_header('Referer', referer)
        request.add_header('User-Agent',"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8")
        response = opener.open(request)
        data = response.read()
        f = open(fileName, 'wb')
        f.write(data)
        print  fileName + "succeed"
        f.close()

if __name__ == "__main__":
    login()
    for i in range(pages):
        print "this is " + str(i+1) + "pages"
        content = getPage(i+1)
        content = content.decode('utf-8')
        images = getImages(content)
        saveImgs(images)
