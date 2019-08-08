#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from urllib import request, parse
import http.cookiejar
import gzip
import re
import json
from html import unescape # unescape is for '&lt;' -> '<'
import os
import tkinter
import tkinter.filedialog

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r', flush = True)
    # Print New Line on Complete
    if iteration == total: 
        print()

        
# Input 
print('****************************')
print('** 2018年新版网络学堂备份 **')
print('**       By: bzy15        **')
print('**     565862568@qq.com   **')
print('****************************')

print('1、选择备份的位置！')

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window
currdir = os.getcwd()
rootDir = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
if len(rootDir) > 0:
    print("你选择了： %s" % rootDir)
else:
    print('默认目录为该目录')
    rootDir = '.'

    
print('2、请输入账号:【如bzy15】')
userName = input()
print('3、请输入密码:')
password = input()

print('4、是否使用本地备份的下载链接文件?')
print('【0】：不使用，【1】：使用。(第一次：0)')
if(input() == '0'):
    print("不使用备份文件！")
    if os.path.exists(os.path.join(rootDir, 'fileList.json')):
        os.remove(path)
else:
    print("使用本地备份文件！")

print('5、保存类型?')
print('【0】：通知+课件+作业')
print('【1】：仅通知')
print('【2】：仅课件')
print('【3】：仅作业')
# control variable
type = input()
if(type == '1'):
    ON_NOTICE = True
    ON_FILE = False
    ON_SUBMIT = False
elif(type == '2'):
    ON_NOTICE = False
    ON_FILE = True
    ON_SUBMIT = False
elif(type == '3'):
    ON_NOTICE = False
    ON_FILE = False
    ON_SUBMIT = True
else:
    ON_NOTICE = True
    ON_FILE = True
    ON_SUBMIT = True
    

print('开始备份!')
## START
# cookiejar
cookiejar = http.cookiejar.CookieJar()
handler = request.HTTPCookieProcessor(cookiejar)
opener = request.build_opener(handler)  # 通过handler来构建opener

## loginAccountSave processing
loginAccountSaveUrl = 'http://learn.tsinghua.edu.cn/f/loginAccountSave'
loginAccountSaveData = parse.urlencode([('loginAccount', userName)])
loginAccountSaveHeader = {
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://learn.tsinghua.edu.cn',
    'Referer': 'http://learn.tsinghua.edu.cn/f/login',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}
    
loginAccountSaveReq = request.Request(loginAccountSaveUrl, data=loginAccountSaveData.encode('UTF-8'), 
    headers=loginAccountSaveHeader, method='POST')

loginAccountSaveRes = opener.open(loginAccountSaveReq)

if loginAccountSaveRes.status == 200:
    print('loginAccountSave OK!')
    
## loginDo processing
loginDoUrl = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do'
loginDoData = parse.urlencode([('i_user', userName), ('i_pass', password), ('atOnce', 'ture')])
loginDoHeader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '40',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'id.tsinghua.edu.cn',
    'Origin': 'http://learn.tsinghua.edu.cn',
    'Referer': 'http://learn.tsinghua.edu.cn/f/login',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

loginDoReq = request.Request(loginDoUrl, data=loginDoData.encode('UTF-8'), 
    headers=loginDoHeader, method='POST')
loginDoRes = opener.open(loginDoReq)

if loginDoRes.status == 200:
    print('loginDo OK!')

if loginDoRes.info().get('Content-Encoding') != 'gzip':
    print('loginDoHtml没有使用gzip压缩')
    loginDoHtml = loginDoRes.read().decode('utf-8')
else:
    # decompress and decode
    print('loginDoHtml使用gzip压缩')
    loginDoHtml = gzip.decompress(loginDoRes.read()).decode('utf-8')
    

# use regex to find ticket and url
regex=re.compile(r'(?<=href=").+(?=">)')
ticketWebUrl = regex.findall(loginDoHtml)[0]
regex=re.compile(r"(?<=ticket=).+$")
ticket = regex.findall(ticketWebUrl)[0]

## ticketWeb process
ticketWebHeader = {
    'Host': 'learn.tsinghua.edu.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

ticketWebReq = request.Request(ticketWebUrl, headers=ticketWebHeader, method='GET')
ticketWebRes = opener.open(ticketWebReq)

## springSecurityRoaming : redirect to http://learn.tsinghua.edu.cn/f/wlxt/index/course/student/
springSecurityRoamingUrl = 'http://learn.tsinghua.edu.cn/b/j_spring_security_thauth_roaming_entry?ticket=' + ticket
ticketWebHeader['Referer'] = ticketWebUrl
springSecurityRoamingReq = request.Request(springSecurityRoamingUrl, headers=ticketWebHeader, method='GET')
springSecurityRoamingRes = opener.open(springSecurityRoamingReq)

if springSecurityRoamingRes.info().get('Content-Encoding') != 'gzip':
    print('springSecurityRoamingHtml没有使用gzip压缩')
    loginDoHtml = springSecurityRoamingRes.read().decode('utf-8')
else:
    # decompress and decode
    print('springSecurityRoamingHtml使用gzip压缩')
    loginDoHtml = gzip.decompress(springSecurityRoamingRes.read()).decode('utf-8')

## pageList process
pageListUrl = 'http://learn.tsinghua.edu.cn/b/wlxt/kc/v_wlkc_xs_xktjb_coassb/pageList'
pageListHeader = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://learn.tsinghua.edu.cn',
    'Referer': 'http://learn.tsinghua.edu.cn/f/wlxt/index/course/student/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
pageListData = parse.urlencode([('aoData', r'[{"name":"sEcho","value":1},{"name":"iColumns","value":5},{"name":"sColumns","value":",,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":"-1"},{"name":"mDataProp_0","value":"function"},{"name":"bSortable_0","value":false},{"name":"mDataProp_1","value":"kcm"},{"name":"bSortable_1","value":true},{"name":"mDataProp_2","value":"jslx"},{"name":"bSortable_2","value":true},{"name":"mDataProp_3","value":"xnxq"},{"name":"bSortable_3","value":true},{"name":"mDataProp_4","value":"jsmc"},{"name":"bSortable_4","value":true},{"name":"iSortingCols","value":0}]')])

pageListReq = request.Request(pageListUrl, data=pageListData.encode('UTF-8'), 
    headers = pageListHeader, method='POST')
pageListRes = opener.open(pageListReq)

if pageListRes.info().get('Content-Encoding') != 'gzip':
    print('pageListHtml没有使用gzip压缩')
    pageListHtml = pageListRes.read().decode('utf-8')
else:
    # decompress and decode
    print('pageListHtml使用gzip压缩')
    pageListHtml = gzip.decompress(pageListRes.read()).decode('utf-8')

    
pageList = json.loads(pageListHtml)
# dict_keys(['result', 'msg', 'object'])

if pageList['result'] == 'success':
    print("pageList success!")

# pageList['object']  : dict_keys(['iTotalRecords', 'iTotalDisplayRecords', 'iDisplayStart', 'iDisplayLength', 'sEcho', 'sSearch', 'aaData'])
print('共有' + pageList['object']['iTotalRecords'] + '门课程!')


courseData = pageList['object']['aaData']
course_xnxq = list(set([course['xnxq'] for course in courseData])) # 学年学期


## creat directory
print('creat directory!')
for xnxq in course_xnxq:
    try:
        os.mkdir(os.path.join(rootDir, xnxq))
    except:
        print('creat '+ os.path.join(rootDir, xnxq) + ' failed!')

# creat file and  homework for all courses      
courseDict = {}
for course in courseData:
    courseDict[course['wlkcid']] = os.path.join(rootDir, course['xnxq'], course['kcm'] + '_' + course['jsm'])
    try:
        os.mkdir(courseDict[course['wlkcid']])
    except:
        print('creat '+ courseDict[course['wlkcid']] + ' failed!')
    try:
        os.mkdir(os.path.join(courseDict[course['wlkcid']], 'file'))
    except:
        print('creat '+ os.path.join(courseDict[course['wlkcid']], 'file') + ' failed!')
    try:
        os.mkdir(os.path.join(courseDict[course['wlkcid']], 'homework'))
    except:
        print('creat '+ os.path.join(courseDict[course['wlkcid']], 'homework') + ' failed!')
                



## download notice
if ON_NOTICE:
    for key, value in courseDict.items():
        noticePageUrl = 'http://learn.tsinghua.edu.cn/b/wlxt/kcgg/wlkc_ggb/student/pageListXs'
        noticePageHeader = {
            'Host': 'learn.tsinghua.edu.cn',
            'Connection': 'keep-alive',
            #'Content-Length': '839',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://learn.tsinghua.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://learn.tsinghua.edu.cn/f/wlxt/kcgg/wlkc_ggb/student/beforePageListXs?wlkcid=%s&sfgk=0' % key,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        }
        noticePageData = parse.urlencode([('aoData', r'[{"name":"sEcho","value":1},{"name":"iColumns","value":3},{"name":"sColumns","value":",,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":"-1"},{"name":"mDataProp_0","value":"bt"},{"name":"bSortable_0","value":true},{"name":"mDataProp_1","value":"fbr"},{"name":"bSortable_1","value":true},{"name":"mDataProp_2","value":"fbsj"},{"name":"bSortable_2","value":true},{"name":"iSortingCols","value":0},{"name":"wlkcid","value":"%s"}]' % key)])
        noticePageReq = request.Request(noticePageUrl, data=noticePageData.encode('UTF-8'), 
            headers = noticePageHeader, method='POST')
        noticePageRes = opener.open(noticePageReq)

        if noticePageRes.info().get('Content-Encoding') != 'gzip':
            # print('noticePageHtml没有使用gzip压缩')
            noticePageHtml = noticePageRes.read().decode('utf-8')
        else:
            # decompress and decode
            # print('noticePageHtml使用gzip压缩')
            noticePageHtml = gzip.decompress(noticePageRes.read()).decode('utf-8')
        noticeData = json.loads(noticePageHtml) # dict_keys(['result', 'msg', 'object'])
        
        with open(os.path.join(value, "notice.html"), "w", encoding='UTF-8') as f:
            f.write("""
                <html>
                <head></head>
                <body>
                """)
            for notice in noticeData['object']['aaData']: 
                f.write("【标题】:%s <br>" % unescape(str(notice['bt'])))
                f.write("【发布人】:%s <br>" % unescape(str(notice['fbr'])))
                f.write("【发布时间】:%s <br>" % unescape(str(notice['fbsj'])))
                f.write("【内容】:%s <br>" % unescape(str(notice['ggnrStr'])))
                f.write("<br><br>")
            f.write("""
                </body>
                </html>
                """) 
        print('%s共有%s条通知, 保存成功' % (value, noticeData['object']['iTotalRecords']))
    print("通知备份完成。")
    
# if exists backup file
if os.path.exists(os.path.join(rootDir, 'fileList.json')):  
    with open(os.path.join(rootDir, 'fileList.json'), 'r', encoding = 'UTF-8') as f:
        fileList = json.loads(f.read())
        print("从备份文件%s中读取下载url！" % os.path.join(rootDir, 'fileList.json'))
else:
    ## fetch file url and size
    fileList = []
    if ON_FILE:
        for key, value in courseDict.items():
            filePageUrl = 'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjflb/student/pageList?wlkcid=%s' % key
            filePageHeader = {
                'Host': 'learn.tsinghua.edu.cn',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'Referer': 'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjflb/student/pageList?wlkcid=%s&sfgk=0' % key,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            }
            filePageReq = request.Request(filePageUrl, headers = filePageHeader, method='GET')
            filePageRes = opener.open(filePageReq)

            if filePageRes.info().get('Content-Encoding') != 'gzip':
                # print('filePageHtml没有使用gzip压缩')
                filePageHtml = filePageRes.read().decode('utf-8')
            else:
                # decompress and decode
                # print('filePageHtml使用gzip压缩')
                filePageHtml = gzip.decompress(filePageRes.read()).decode('utf-8') 
            filePageData = json.loads(filePageHtml)
            print('%s课件共有%s个分类' % (value, filePageData['object']['records']))
            # create directory and fetch download url
            for classification in filePageData['object']['rows']:
                # for all classification extract its download url
                fileListUrl = 'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/kjxxb/%s/%s' % (key, classification['id'])
                fileListHeader = {
                    'Host': 'learn.tsinghua.edu.cn',
                    'Connection': 'keep-alive',
                    'Accept': '*/*',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                    'Referer': 'http://learn.tsinghua.edu.cn/f/wlxt/kj/wlkc_kjxxb/student/beforePageList?wlkcid=%s&sfgk=0' % key,
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                }
                fileListReq = request.Request(fileListUrl, headers = fileListHeader, method='GET')
                fileListRes = opener.open(fileListReq)
                if springSecurityRoamingRes.info().get('Content-Encoding') != 'gzip':
                    # print('filePageHtml没有使用gzip压缩')
                    fileListHtml = fileListRes.read().decode('utf-8')
                else:
                    # decompress and decode
                    # print('filePageHtml使用gzip压缩')
                    fileListHtml = gzip.decompress(fileListRes.read()).decode('utf-8') 
                fileListData = json.loads(fileListHtml)
                print('%s分类下共有%d个文件' % (classification['bt'], len(fileListData['object'])))
                
                if len(fileListData['object']) > 0: # create directory 
                    try:
                        os.mkdir(os.path.join(value, 'file', classification['bt']))
                    except:
                        print('creat '+ os.path.join(value, 'file', classification['bt']) + ' failed!')
                        
                for fileObject in fileListData['object']:
                    fileList.append(
                        {'url':'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid=%s' % fileObject[7], 
                        'ref': 'http://learn.tsinghua.edu.cn/f/wlxt/kj/wlkc_kjxxb/student/beforePageList?wlkcid=%s&sfgk=0' % fileObject[4],
                        'size': fileObject[9], 'name':fileObject[1], 'dir':os.path.join(value, 'file', classification['bt'])} 
                    )

    ## fetch submitted file url and size
    submitList = []
    if ON_SUBMIT:
        for key, value in courseDict.items():          
            zyListYjwgUrl = 'http://learn.tsinghua.edu.cn/b/wlxt/kczy/zy/student/zyListYjwg'    
            zyListYpgUrl = 'http://learn.tsinghua.edu.cn/b/wlxt/kczy/zy/student/zyListYpg'  
            
            zyListHeader = {
                'Host': 'learn.tsinghua.edu.cn',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://learn.tsinghua.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'http://learn.tsinghua.edu.cn/f/wlxt/kczy/zy/student/beforePageList?wlkcid=%s' % key,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            }
            zyListData = parse.urlencode([('aoData', r'[{"name":"sEcho","value":1},{"name":"iColumns","value":8},{"name":"sColumns","value":",,,,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":"-1"},{"name":"mDataProp_0","value":"wz"},{"name":"bSortable_0","value":false},{"name":"mDataProp_1","value":"bt"},{"name":"bSortable_1","value":true},{"name":"mDataProp_2","value":"mxdxmc"},{"name":"bSortable_2","value":true},{"name":"mDataProp_3","value":"zywcfs"},{"name":"bSortable_3","value":true},{"name":"mDataProp_4","value":"kssj"},{"name":"bSortable_4","value":true},{"name":"mDataProp_5","value":"jzsj"},{"name":"bSortable_5","value":true},{"name":"mDataProp_6","value":"jzsj"},{"name":"bSortable_6","value":true},{"name":"mDataProp_7","value":"function"},{"name":"bSortable_7","value":false},{"name":"iSortCol_0","value":5},{"name":"sSortDir_0","value":"desc"},{"name":"iSortCol_1","value":6},{"name":"sSortDir_1","value":"desc"},{"name":"iSortingCols","value":2},{"name":"wlkcid","value":"%s"}]' % key)])
            # 已交未改
            zyListYjwgReq = request.Request(zyListYjwgUrl, data=zyListData.encode('UTF-8'), 
                headers = zyListHeader, method='POST')
            zyListYjwgRes = opener.open(zyListYjwgReq)
            if zyListYjwgRes.info().get('Content-Encoding') != 'gzip':
                zyListYjwgHtml = zyListYjwgRes.read().decode('utf-8')
            else:
                zyListYjwgHtml = gzip.decompress(zyListYjwgRes.read()).decode('utf-8') 
            # print(zyListYjwgHtml)
            zyListYjwgData = json.loads(zyListYjwgHtml)
            print('共有%s条未批改的作业' % zyListYjwgData['object']['iTotalRecords'])
            
            # 已批改
            zyListYpgReq = request.Request(zyListYpgUrl, data=zyListData.encode('UTF-8'), 
                headers = zyListHeader, method='POST')
            zyListYpgRes = opener.open(zyListYpgReq)
            if zyListYpgRes.info().get('Content-Encoding') != 'gzip':
                zyListYpgHtml = zyListYpgRes.read().decode('utf-8')
            else:
                zyListYpgHtml = gzip.decompress(zyListYpgRes.read()).decode('utf-8') 
            # print(zyListYpgHtml)
            zyListYpgData = json.loads(zyListYpgHtml)
            print('共有%s条已批改的作业' % zyListYpgData['object']['iTotalRecords'])
            
            # combine them together and extract download url
            zyListData = zyListYpgData['object']['aaData'] + zyListYjwgData['object']['aaData']
            for homework in zyListData:
                if homework['zyfjid'] != "" and homework['zyfjid'] is not None: # has attachment
                    submitList.append(
                        {'url': 'http://learn.tsinghua.edu.cn/b/wlxt/kczy/zy/student/downloadFile/%s/%s' % (homework['wlkcid'], homework['zyfjid']),
                        'ref': 'http://learn.tsinghua.edu.cn/f/wlxt/kczy/zy/student/viewCj?wlkcid=%s&zyid=%s&xszyid=%s' % (homework['wlkcid'], homework['zyid'], homework['xszyid']),
                        'name': homework['wjmc'],
                        'size': homework['wjdx'],
                        'dir': os.path.join(value, 'homework')
                        }
                    )
         
    ## backup    
    fileList = fileList + submitList
    if fileList != []:
        with open(os.path.join(rootDir, 'fileList.json'), 'w', encoding = 'UTF-8') as f:
            f.write(json.dumps(fileList))  
            print("将下载url备份到文件%s中！" % os.path.join(rootDir, 'fileList.json'))


## download files and submitted files
fileHeader = {
    'Host': 'learn.tsinghua.edu.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}
regex=re.compile(r'(?<=filename=").+(?="$)')

blocksize = 4096
num = 0;
print("待下载的共%d个文件" % len(fileList))
for fileDict in fileList:
    num += 1
    tempHeader = fileHeader.copy()
    tempHeader['Referer'] = fileDict['ref']
    fileReq = request.Request(fileDict['url'], headers=tempHeader, method='GET')
    fileRes = opener.open(fileReq)
    file_name = regex.findall(fileRes.getheader('Content-Disposition'))[0]
    file_name = file_name.encode('latin-1').decode('utf-8')
    if os.path.exists(os.path.join(fileDict['dir'], file_name)):
        print("(%d/%d)已经存在文件:%s" % (num, len(fileList), file_name))
        continue
    print('(%d/%d)开始保存文件:%s, 文件大小%.3fMB' % (num, len(fileList), file_name, int(fileDict['size']) / 1024 / 1024))  
    print('(%d/%d)保存路径:%s,' % (num, len(fileList), os.path.join(fileDict['dir'], file_name)))  
    with open(os.path.join(fileDict['dir'], file_name), 'wb') as f:
        file_size = 0  
        while True:
            buffer = fileRes.read(blocksize)
            if not buffer:
                break
            f.write(buffer)
            file_size += len(buffer)
            printProgressBar(file_size , int(fileDict['size']))
            