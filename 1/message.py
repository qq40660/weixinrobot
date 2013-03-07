#coding: utf-8
import web
import hashlib, urllib2
import sys, os, time
from lxml import etree
import re,json

best_login_url = "http://handset2.appl.800best.com/htgprs2/UserValidation.ashx?username=999996&password=938D819B43F403E586FA498F55DBDCCE&site=999996&guid=D310C1J003&version=4.1"

best_bill_check_url = "http://handset2.appl.800best.com/htgprs2/TrackBill.ashx?username=%s&token=%s&billcode=%s&guid=%s&version=4.54"
token = "fa88f8478ccf34014103393ff0c706fd"
result_text = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
            </xml>"""

welcome_msg = u"welcome"
class bill_info:
    user_name = None
    token = None
    guid = "weixin"
class get_message:

    is_login = False
    bill = None
    def GET(self):
        param = web.input()
        p_list = [token]
        echostr = param.echostr
        signature = param.ignature
        timestamp = param.timestamp
        nonce = param.nonce
        p_list.append(timestamp)
        p_list.append(nonce)
        p_list.sort()
        p_list.sort()
        sec_str = "".join(p_list)
        hashstr = hashlib.sha1(sec_str).hexdigest()
        if hashstr == signature:
            return echostr
        print signature,timestamp,nonce
        print sec_str,hashstr

        return "Error" + echostr

    def POST(self):
        data = web.data()
        print data
        root = etree.fromstring(data)
        children = list(root)
        recive = {}
        for child in children:
            recive[child.tag] = child.text
        if not recive.has_key("Content"):
            return None
        content = recive['Content']
        if content == "Hello2BizUser":
            result = welcome_msg
            echostr = result_text % (recive['FromUserName'], recive['ToUserName'],recive['CreateTime'],recive['MsgType'],result)
            return echostr
        pattern = re.compile(r'\d+')
        match = pattern.search(content)
        if match:
            bill_id = match.group()
            bill_result = self.get_bill_info(bill_id)
            result = ""
            for b in bill_result:
                result += b["TrackTime"].encode("utf-8") + "\n"
                result += b["Description"].encode("utf-8") + "\n\n"

            print result
            #result = match.group()

        echostr = result_text % (recive['FromUserName'], recive['ToUserName'],recive['CreateTime'],recive['MsgType'],result)
        return echostr

    def get_bill_info(self, bill_id):
        if self.bill == None:
            self.bill_login()
        if self.bill == None:
            return None
        bill_url = best_bill_check_url %(self.bill.user_name, self.bill.token, bill_id, self.bill.guid)

        bill_r = urllib2.urlopen(bill_url)
        bill_result = json.loads(bill_r.read())
        if bill_result["ServerFlag"] != 0:
            self.bill_login()
            if self.bill != None:
                bill_r = urllib2.urlopen(bill_url)
                bill_result = json.loads(bill_r.read())
        result = ""
        for b in bill_result["TrackResultList"]:
            result += b["TrackTime"].encode("utf-8") + "\n"
            result += b["Description"].encode("utf-8") + "\n\n"

        print result.decode("utf-8").encode("gb2312")
        return bill_result["TrackResultList"]

    def bill_login(self):
        r = urllib2.urlopen(best_login_url)
        login_info = json.loads(r.read())
        if not login_info["IsSuccess"]:
            return None
        self.bill = bill_info()
        self.bill.user_name = login_info['UserName']
        self.bill.token = login_info["Token"]

if __name__ == "__main__":
    msg = get_message()
    msg.get_bill_info(210164181510)

