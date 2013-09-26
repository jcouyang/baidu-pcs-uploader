import os
import json
import subprocess
import requests
from config import *
from os.path import join, getsize
for root, dirs, files in os.walk('/mnt/data/torrents'):
    for name in files:
        if not '.config' in root :
            print root+'/'+name
            if True:#getsize(join(root,name)) < 2000000000:
                subprocess.call(["curl", "-k", "-F",'file=@'+join(root,name), 'https://pcs.baidu.com/rest/2.0/pcs/file?method=upload&access_token='+TOKEN+'&path=/apps/uploaded/'+name])
            else:
                file = open(join(root,name),'rb')
                filearray = []
                while (True):
                    blockfile = file.read(2000000000)
                    if not blockfile:
                        break
                    fileblock = {'file':blockfile}
                    upload = requests.post("https://pcs.baidu.com/rest/2.0/pcs/file?method=upload&access_token="+TOKEN+"&type=tmpfile", files=fileblock)
                    filearray.append(upload.json()['md5'])
                combine_file =requests.post('https://pcs.baidu.com/rest/2.0/pcs/file?method=createsuperfile&access_token='+TOKEN+'&path=/apps/uploaded/combine.jpg&param={"block_list":'+json.dumps(filearray)+'}')
