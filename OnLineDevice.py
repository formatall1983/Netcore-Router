#! python3
#coding:utf-8
import requests
import os
import traceback
import re
import time
import itchat

url='http://baohope:Lk1+2+3+4=10@192.168.1.1/router/dhcp_dynamicip_show.cgi'
MACWithName={'74-A5-28-31-45-E6':'huawei honer 7',
             'E4-46-DA-51-76-40':'小米MIX2',
             '00-30-18-AB-40-32':'我的电脑',
             'C0-3F-D5-B7-28-04':'陈虹宇的电脑',
             'C0-3F-D5-BA-B1-18':'财务电脑 1/4',
             '74-27-EA-B5-65-BE':'小波的电脑',
             'BC-E6-3F-D6-66-B7':'小波的手机',
             'B4-A3-82-BB-E9-16':'海康威视',
             '30-05-5C-9C-AA-CA':'打印机兄弟',
             '00-80-F0-19-FA-30':'打印机',
             'BC-3A-EA-C9-04-47':'陈虹宇的手机',
             '74-27-EA-B9-30-FF':'领导的电脑',
             'A8-BE-27-BD-B3-F6':'领导的手机',
             'B0-48-1A-4F-AD-2E':'陈益华的手机',
             '74-27-EA-B9-4E-C5':'俞师傅的电脑',
             'E0-19-1D-F6-38-7D':'荣耀畅玩4X',
             '74-27-EA-B6-9C-63':'俞师傅的手机',
             'B8-08-D7-41-AC-B3':'俞师傅另外一个手机',
             'B8-27-EB-2D-1B-87':'树莓派zero WH',
             '48-5A-3F-32-66-03':'应该是领导的手机'}


def BL(url):   #核心函数,从路由器获得设备的mac地址和在线的状态
    dec={}
    try:
        b=requests.post(url)
    except:
        b=traceback.format_exc()
        a=re.findall("mac.*?end",b)
        b=0
        for macip in a:
            mac=macip[6:23]
            active=macip[-7:-6]
            if active=='1':
                mac=PP(mac)
                dec[mac]=active
            b=b+1
        #print(b)
    return dec

def PP(mac):    #用来把mac地址替换成已知的设备名,否则查询到的只是mac地址,不知道是啥设备
        mac=mac.replace(key,value)
    return mac

def final(allmac):  #最后把所有在线的设备打包成一个文本变量
    mac="当前在线的设备"+"\n"
    for key in allmac:
        mac=mac+key+'\n'
    mac=mac+time.strftime('%Y-%m-%d %H:%M:%S')
    return mac

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    name=FindName('format_all')
    print(msg['Text'])
    a=final(BL(url))
    #print(a)
    itchat.send_msg(msg=a,toUserName=name)

def FindName(name):     #从微信好友列表中找出format_all的ID,类似于@XXXXXXXXXXXXXXXX的状态的内容,这样就可以用itchat库给自己主号发送微信,这里有个注意点
    #itchat.auto_login(hotReload=True, enableCmdQR=2)
    tmp=itchat.get_friends()
    MainName=name
    for key in tmp:
        name=MainName   #这里要注意,循环里如果没有这一句,会出错.因为后面re.search后,name被清空
        key=str(key)
        fri=str(re.search(name,key))
        if fri != 'None':
            name=str(re.search('@.{32}',key))[-35:-2]
            break
    return name

itchat.auto_login(hotReload=True,enableCmdQR=2)
itchat.run()
