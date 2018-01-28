
import urllib2, json, time, os, sys

app_id = ""
appsecret = ""

def wechat_template(open_id,access_token,link_url=None,HOST_ip=None,error_p=None,error_v=None,error_time=None,*args):
    template_id = "5zXcSMf2khfjxazSYN-2O3DDNY0NJ9Ua6LMGo0cCKSI"
    wechat_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token

    json_data = {"touser":open_id,
                 "template_id": template_id,
                 "url": link_url,
                 "topcolor": "#FF0000",
                 "data":{
                     "HOST_IP": {
                         "value":HOST_ip,
                         "color":"#173177"
                     },
                     "error_p":{
                         "value":error_p,
                         "color":"#173177"
                     },
                     "error_v":{
                         "value":error_v,
                         "color":"#173177"
                     },
                     "error_time":{
                         "value":error_time,
                         "color":"#173177"
                     }
                 }
                 }

    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=wechat_url,headers=headers,data=json.dumps(json_data))
    response = urllib2.urlopen(request)
    return response.read()


def wechat_get_open_id(access_token):
    wechat_url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=" + access_token
    wechat_user_json = urllib2.urlopen(wechat_url)
    wechat_user_dict = json.loads(wechat_user_json.read())
    #print wechat_user_dict.has_key("data")
    if "data" in wechat_user_dict.keys():
        return wechat_user_dict["data"]["openid"]
    else:
        return wechat_user_dict["errcode"]

def wechat_access_token_get():
    wechat_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+ app_id + "&secret=" + appsecret
    def access_token_get():
        wechat_access_token_json = urllib2.urlopen(wechat_url)
        wechat_access_token_dict = json.loads(wechat_access_token_json.read())
        return wechat_access_token_dict
    wechat_access_token_dict = access_token_get()
    while True:
        if "access_token" in wechat_access_token_dict.keys():
            return wechat_access_token_dict["access_token"]
        else:
            #return wechat_access_token_dict["errcode"]
            time.sleep(5)
            wechat_access_token_dict = access_token_get()

def info_write_file(operation,access_token=None):
    if operation == "w":
        file_name = open("./wechat_access_token.info","w")
        file_name.write(access_token)
        file_name.close()
        return access_token
    elif operation == "r":
        file_name = open("./wechat_access_token.info","r")
        access_token = file_name.read()
        file_name.close()
        return access_token

def access_token_isfile(file_name):
    if os.path.isfile(file_name):
        return 0
    else:
        return 1

def access_token_expire():
    DATE_DQ = int(time.time())
    access_token_file = access_token_isfile("./wechat_access_token.info")
    def access_token_g():
        access_token_get = wechat_access_token_get()
        access_token_w = access_token_get + "---" + str(DATE_DQ)
        access_token = info_write_file("w", access_token_w)
        return access_token_get

    if access_token_file == 0:
        access_token_s = info_write_file("r")
        access_token = access_token_s.split("---")
        if (DATE_DQ - int(access_token[1])) < 7000:
            return access_token[0]
        else:
            access_token = access_token_g()
            return access_token
    else:
        access_token = access_token_g()
        return access_token

if __name__ == "__main__":
    opt = len(sys.argv)
    if opt == 6:
        access_token = access_token_expire()
        #print access_token
        wechat_user = wechat_get_open_id(access_token)
        if isinstance(wechat_user,list):
            for I in wechat_user:
               jg =  wechat_template(I,access_token,sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
               print jg
            #print wechat_user
        else:
            print "error: ", wechat_user
    else:
        pass