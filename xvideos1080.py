#coding=utf-8
import requests
import re
import os
import shutil
import time

#播放地址
url_play = 'https://www.xxxxxxxxxxxxxxxxxxxxxxxxse_maids_in_my_house_part_1'

#低画质下载地址,需要登录获取下载地址
url_down_low = 'https://xxxxxxxxxxxxxxxx9&download=1'

url_play = input('请输入播放地址：\n')
url_down_low =input("请输入低品质下载地址：\n")

#获取请求参数
info = '?' + re.search('e=(.*)',url_down_low).group()
print(info)

#获取画质列表文件地址
res0 = requests.get(url_play).text
a1 = re.search('https://hls(.*)\'',res0)
url_m3u8 = a1.group().replace('\'','')
print(url_m3u8)

#获取画质列表中1080p画质名称
res1 = requests.get(url_m3u8).text
a2 = re.search('(.*)1080p.m3u8(.*)',res1).group()
print(a2)


#构建获取ts列表地址
if '?' in a2:
    url_ts = url_m3u8.split('hls.m3u8')[0] + a2
    print(url_ts)
    print(1)

else:
    url_ts = url_m3u8.replace('hls.m3u8', a2) + info
    print(url_ts)
    print(2)

#获取ts列表内容
res2 = requests.get(url_ts).text

#统计ts数量
ts_list = re.findall('hls.*.ts.*',res2)
print('ts_list:',ts_list)
cont = len(ts_list) -1
# print(cont)

#构建ts下载地址列表
ts_url_list = []
for ts in ts_list:
    if '?' in ts:
        tsurl = url_m3u8.split('hls.m3u8')[0] + ts
    else:
        tsurl = url_m3u8.replace('hls.m3u8',ts) + info
    ts_url_list.append(tsurl)
print(ts_url_list)

###########################download#############################
#临时目录
if os.path.exists('tmp'):
    shutil.rmtree('tmp')
    time.sleep(1)
    os.makedirs('tmp')
else:
    os.makedirs('tmp')

#开始下载
print('downloading...cont {}'.format(cont))
i = 0
for t,u in zip(ts_list,ts_url_list):

    if '?' in t:
        t = t.split('?')[0]

    print('downloading  {}'.format(t))
    try:
        res666 = requests.get(u)

        if i >= 9:
            with open('./tmp/{}'.format(t),'wb') as f:
                f.write(res666.content)
        else:
            tt = list(t)
            tt.insert(-4,'0')
            t = ''.join(tt)
            with open('./tmp/{}'.format(t), 'wb') as f:
                f.write(res666.content)
            i += 1

    except:
        print('download {} error'.format(t))

###########################合并#################################
#合并为mp4视频文件
os.system('copy /b  tmp\\*.ts ' + ' 1080p{}.mp4'.format(str(time.time())))