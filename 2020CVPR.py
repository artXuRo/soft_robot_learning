# -*- coding: utf-8 -*-
import re
import requests
import urllib.request
import os
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--keyword',type=str, default='detection')
#传参匹配
args = parser.parse_args()

#获得网页信息
r = requests.get('http://openaccess.thecvf.com/CVPR2020.py')
#信息保存在json文件里，没有保存在text因为我不喜欢
data = r.text
#获取PDF links
linklist = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)" ,data)
namelist = re.findall(r"(?<=href=\").+?2020_paper.html\">.+?</a>" ,data)

cnt = 0
num = len(linklist)

#local path
localpath = './CVPR2020/{}/'.format(args.keyword)
if not os.path.exists(localpath):
    os.makedirs(localpath)
while cnt < num:
    url = linklist[cnt] # define download url
    filename = namelist[cnt].split('<')[0].split('>')[1]# distribute file name from list
    filename = filename.replace(':','_')
    filename = filename.replace('\"','_')   
    filename = filename.replace('?','_')
    filename = filename.replace('/','_') 
    filename = filename.replace('+','_')
    filename = filename.replace(' ','_')
    searchlist = filename.split('_')
    searchmodel = re.compile(r'{}'.format(args.keyword),re.IGNORECASE)
    
    download_next_paper = True
    
    if ([True for i in searchlist if searchmodel.findall(i)]):
        download_next_paper = False
        
    if download_next_paper:
        cnt += 1
        continue
        
    filepath = localpath + filename + '.pdf'
    if os.path.exists(filepath):
        print('file [{}.pdf] exist, skip downloading')
        cnt += 1
        continue
    else:
        print('['+str(cnt)+"/"+str(num)+"] Downloading -> "+filepath)
        try:
        
            urllib.request.urlretrieve('http://openaccess.thecvf.com/'+url,filepath)
        except :
            print('download failed: ' + filepath)
        cnt += 1
        
print('finished')
