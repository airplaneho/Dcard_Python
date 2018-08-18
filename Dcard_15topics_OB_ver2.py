# -*- coding: utf-8 -*-
#Dcard_15topics_OB_ver2.py
#執行會爬Dcard的15個主題的文章，每個主題50篇最新文章
#輸出15個主題的./Dcard_Json/name/time.json
from multiprocessing import Pool  
import time,requests,os,json
from bs4 import BeautifulSoup
def task1(name):
    print(name,"Start : %s" % time.ctime())
    if not os.path.exists('./Dcard_Json/'+name):
        os.makedirs('./Dcard_Json/'+name)
    url="https://www.dcard.tw/_api/forums/"+name+"/posts?popular=false&limit=50"
    res= requests.get(url)
    data=[]
    data=res.json() 
    id_list=[]
    for i in range(50):
        id_list.append(data[i]['id'])
    all_post=[]
    for id in id_list:
        url="https://www.dcard.tw/_api/posts/"+str(id)
        res= requests.get(url)
        data=[]
        data=res.json()
        all_post.append(data)
    output_time=time.strftime("%Y%m%d%H%M",time.localtime())
    with open('./Dcard_Json/'+name+'/'+output_time+'.json','w',encoding='utf-8') as fp:
        json.dump(all_post,fp,sort_keys=False,indent=10,ensure_ascii=False)
    print(name,"End : %s" % time.ctime())

if __name__=='__main__': 
    forum_name=['makeup','travel','money','sport','tvepisode','3c','acg','game','vehicle','movie','boy','girl','food','talk','buyonline',]
    # forum_name=['makeup','talk','buyonline','food',] 
    if not os.path.exists('./Dcard_Json'):
        os.makedirs('./Dcard_Json/')
    print ('父程序Parent process %s'%os.getpid())
    p1=Pool()  
    for name in forum_name:
        p1.apply_async(task1,args=(name,))               
    print ('正等待所有子程序完成 Waiting for all subprocess done ...')
    p1.close()  
    p1.join()  
    print ('所有子程序已經完成 All subprocess done' )