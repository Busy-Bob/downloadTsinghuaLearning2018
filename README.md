# downloadTsinghuaLearning2018
- 用于备份清华大学新版网络学堂(2018年版)。
- 可备份**公告/课件/上传作业**
- 用pyinstaller生成了exe文件在./dist目录下。
## 背景
- 听说网络学堂在毕业一年后就不能登陆了，于是想要全部内容都备份一份
- 今年网络学堂变成2018年新版，网络上的备份软件不能使用了。
## 登陆流程
利用chrome抓包，分析出登录流程如下：
- http://learn.tsinghua.edu.cn/f/loginAccountSave POST请求，DATA：loginAccount=XXX
- https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do POST请求，DATA：[('i_user', userName), ('i_pass', password), ('atOnce', 'ture')], 返回数据为带ticket的自动跳转html页面(被gzip压缩)。
- 'http://learn.tsinghua.edu.cn/b/j_spring_security_thauth_roaming_entry?ticket=' + ticket, GET请求，用于安全登陆，成功后会302重定向到网络学堂首页：http://learn.tsinghua.edu.cn/f/wlxt/index/course/student/ ，完成了登陆过程。

## 通知、课件、上传作业
- DATA中的 {"name":"iDisplayLength","value":"-1"}，是为了请求全部列表。
- http://learn.tsinghua.edu.cn/b/wlxt/kc/v_wlkc_xs_xktjb_coassb/pageList POST请求，DATA：略。可以请求到已修课程列表。
- http://learn.tsinghua.edu.cn/b/wlxt/kcgg/wlkc_ggb/student/pageListXs POST请求，DATA：略。可以请求到通知列表。
- 'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjflb/student/pageList?wlkcid=%s' % key GET请求。可以拉取课件页。
- 'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/kjxxb/%s/%s' % (key, classification['id']) GET请求。可以请求课件页的文件列表。
- http://learn.tsinghua.edu.cn/b/wlxt/kczy/zy/student/zyListYjwg 与 http://learn.tsinghua.edu.cn/b/wlxt/kczy/zy/student/zyListYpg
 POST 请求，DATA：略。可以获得已交未改、已批改文件列表。（省略了未提交）

## 已知问题
- 不能保存作业老师的附件。(需要BS4简单解析一下网页，因为情况太少所以没有做)
