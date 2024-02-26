from src.IniFileUtils import write_ini_file, read_ini_file, update_ini_file, \
    append_multiple_to_ini_file


def init_Configs():
    Normal = {
        'Normal':{
            'username': ' ',
            'password': ' ',
            'nasId': '',
            'isRemember': 'False',
            'isBack': 'False',
            'isStartUp': 'False',
            'isWebAutoLogin': 'False',
            'selectedTheme': '11',
        }
    }
    write_ini_file('config.ini', Normal)

def read_Configs():
    configs = read_ini_file('config.ini')
    return configs['Normal']
def update_Config(config,data):
    update_ini_file('config.ini','Normal',config,data)
def update_Service(web,url,user):
    update_ini_file('config.ini', 'ServiceList', web, {'platUrl':url,
                           'useUser':user})
def read_Services():
    configs = read_ini_file('config.ini')
    print(len(configs.items()))
    if (len(configs.items())<2):
        init_Configs()
        init_Services()
        init_Users()
        configs = read_ini_file('config.ini')
    return configs['ServiceList']
def init_Services():
    ServiceList = {
        'ServiceList': {
            '智慧理工大': {'platUrl':'http://zhlgd.whut.edu.cn/',
                           'useUser':'智慧理工大'},
            '教务系统（智慧理工大）': {'platUrl':'http://sso.jwc.whut.edu.cn/Certification/index2.jsp',
                           'useUser':'智慧理工大'},
            '教务系统': {'platUrl': 'http://sso.jwc.whut.edu.cn/Certification/toIndex.do',
                           'useUser': '教务处'},
            '教务系统(新)': {'platUrl': 'http://jwxt.whut.edu.cn',
                           'useUser': '智慧理工大'},
            '缴费平台': {'platUrl': 'http://cwsf.whut.edu.cn',
                           'useUser': '智慧理工大'},
            '智慧学工': {'platUrl': 'https://talent.whut.edu.cn/',
                           'useUser': '智慧理工大'},
            'WebVPN': {'platUrl': 'https://webvpn.whut.edu.cn/',
                           'useUser': 'WebVPN'},
            '学校邮箱': {'platUrl': 'https://qy.163.com/login/',
                           'useUser': '学校邮箱'},
            '学校主页': {'platUrl': 'http://i.whut.edu.cn/',
                           'useUser': '智慧理工大'},
            '校园地图（智慧理工大版）': {'platUrl': 'http://gis.whut.edu.cn/index.shtml',
                           'useUser': '智慧理工大'},
            '校园地图（微校园版）': {'platUrl': 'http://gis.whut.edu.cn/mobile/index.html#/',
                           'useUser': '智慧理工大'},
            '成绩查询': {'platUrl': 'http://zhlgd.whut.edu.cn/tp_up/view?m=up#act=up/sysintegration/queryGrade',
                                   'useUser': '智慧理工大'},
            '理工智课(小雅)': {'platUrl': "http://zhlgd.whut.edu.cn/tpass/login?service=https%%3A%%2F%%2Fwhut.ai-augmented.com%%2Fapi%%2Fjw-starcmooc%%2Fuser%%2Fcas%%2Flogin%%3FschoolCertify%%3D10497%%26rememberme%%3Dfalse",
                         'useUser': '智慧理工大'},
            '网络教学平台': {
                'platUrl': "https://jxpt.whut.edu.cn/meol/homepage/common/sso_login.jsp",
                'useUser': '智慧理工大'},
        }
    }
    append_multiple_to_ini_file('config.ini', ServiceList)
def update_User(platform,username,password):
    update_ini_file('config.ini',platform,'username',username)
    update_ini_file('config.ini', platform, 'password', password)
def read_Users():
    configs = read_ini_file('config.ini')
    config = {}
    for section in configs.sections():
        print(f"Section: {section}")
        for key in configs[section]:
            # print(key)
            if(key.find('namejs')!=-1):
                print(section)
                config[section] = configs[section]
            # print(f"  {key} = {config[section][key]}")
    for section in config.keys():
        print(f"user: {section}")
        for key in configs[section]:
            print(f"  {key} = {config[section][key]}")
    return config
def init_Users():
    platform = {
        '智慧理工大': {
            'username':'',
            'password':'',
            'nameJs':"document.getElementById('un').value =",
            'passJs':"document.getElementById('pd').value =",
            'loginJs':"document.getElementById('index_login_btn').click();"
        },
        '校园网': {
            'username': '',
            'password': '',
            'nameJs': "document.getElementById('username').value =",
            'passJs': "document.getElementById('password').value =",
            'loginJs': "checkForm();"
        },
        'WebVPN': {
            'username': '',
            'password': '',
            'nameJs': "document.getElementsByName('username')[0].value =",
            'passJs': "document.getElementsByName('password')[0].value =",
            'loginJs': "document.getElementsByName('remember_cookie')[0].click();\n" +
                            "document.getElementById('login').click()"
        },
        '教务处': {
            'username': '',
            'password': '',
            'nameJs': "document.getElementById('username').value =",
            'passJs': "document.getElementById('password').value =",
            'loginJs': "setTimeout(function() {" +
                            "document.getElementById('submit_id').click()" +
                            "}, 1000);"
        },
        '学校邮箱': {
            'username': '',
            'password': '',
            'nameJs': "document.getElementById('accname').value =",
            'passJs': "document.getElementById('accpwd').value =",
            'loginJs': "document.getElementById('accautologin').checked" +
                            "document.getElementsByClassName('u-logincheck logincheck js-logincheck js-loginPrivate loginPrivate')[0].click();\n" +
                            "document.getElementsByClassName('w-button w-button-account js-loginbtn')[0].click();"
        }
    }
    append_multiple_to_ini_file('config.ini', platform)
if __name__ == '__main__':
    # init_Configs()
    # init_Services()
    # init_Users()
    read_Users()
    # config = read_Configs()
    #print(config['nasId'])
    # services = read_Services()
    # for service in services.items():
    #     print(service)

