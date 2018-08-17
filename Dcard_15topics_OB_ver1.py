# -*- coding: utf-8 -*-
#Dcard_15topics_OB_ver1.py
#第一次執行會爬Dcard的15個主題的文章，每個主題100篇最新文章
#第一次輸出15個主題的./Dcard_Json/'+name+'_dcard_1.json所需時間為60~75s
#第二次開始對比第一次輸出的JSON,若有最新文章則只輸出最新文章,若無最新文章則只輸出上次最新文章的'id'
from multiprocessing import Pool  
import time,requests,os,json
from bs4 import BeautifulSoup
def task1(name):
    print(name,"Start : %s" % time.ctime())
    isprevious=0
    isSame=0
    json_file_name='./Dcard_Json/'+name+'_dcard_2.json'
    if os.path.exists(json_file_name):
        isprevious=1
        with open(json_file_name, 'r',encoding='utf-8') as fp:
            previous_data = json.load(fp)

    url="https://www.dcard.tw/_api/forums/"+name+"/posts?popular=false&limit=100"
    res= requests.get(url)
    data=[]
    data=res.json() 
    id_list=[]
    if isprevious==1:
        for i in range(100):        #固定100篇文章
            if  previous_data[0]['id']==data[0]['id']:
                isSame=1
                break
            elif  previous_data[0]['id']==data[i]['id']:
                break
            else:
                id_list.append(data[i]['id'])
    elif isprevious==0:
        for i in range(100):        #固定100篇文章
            id_list.append(data[i]['id'])
    if isSame==0:
        all_post=[]
        for id in id_list:
            url="https://www.dcard.tw/_api/posts/"+str(id)
            res= requests.get(url)
            data=[]
            data=res.json()
            all_post.append(data)
    elif isSame==1:
        all_post=[{'id':previous_data[0]['id']},{'id':previous_data[0]['id']}]
    with open('./Dcard_Json/'+name+'_dcard_1.json','w',encoding='utf-8') as fp:
        json.dump(all_post,fp,sort_keys=False,indent=10,ensure_ascii=False)
    print(name,"End : %s" % time.ctime())

def task2(name): 
    print(name,"Start : %s" % time.ctime())
    isSame=0
    json_file_name='./Dcard_Json/'+name+'_dcard_1.json'
    with open(json_file_name, 'r',encoding='utf-8') as fp:
        previous_data = json.load(fp)
    url="https://www.dcard.tw/_api/forums/"+name+"/posts?popular=false&limit=100"
    res= requests.get(url)
    data=[]
    data=res.json() 
    id_list=[]
    for i in range(100):        #固定100篇文章
        if  previous_data[0]['id']==data[0]['id']:
            isSame=1
            break
        elif  previous_data[0]['id']==data[i]['id']:
            break
        else:
            id_list.append(data[i]['id'])
    if isSame==0:
        all_post=[]
        for id in id_list:
            url="https://www.dcard.tw/_api/posts/"+str(id)
            res= requests.get(url)
            data=[]
            data=res.json()
            all_post.append(data)
    elif isSame==1:
        all_post=[{'id':previous_data[0]['id']},{'id':previous_data[0]['id']}]
    with open('./Dcard_Json/'+name+'_dcard_2.json', 'w',encoding='utf-8') as fp:
        json.dump(all_post,fp,sort_keys=False,indent=10,ensure_ascii=False)
    print(name,"End : %s" % time.ctime())

if __name__=='__main__': 
    forum_name=['makeup','travel','money','sport','tvepisode','3c','acg','game','vehicle','movie','boy','girl','food','talk','buyonline',]
    if not os.path.exists('./Dcard_Json'):
        os.makedirs('./Dcard_Json')
    isnew=0
    while True:
        if isnew==0:
            print ('父程序Parent process %s'%os.getpid())
            p1=Pool()  
            for name in forum_name:
                p1.apply_async(task1,args=(name,))               
            print ('正等待所有子程序完成 Waiting for all subprocess done ...')
            p1.close()  
            p1.join()  
            print ('所有子程序已經完成 All subprocess done' )
            isnew=1
        elif isnew==1:
            print ('\n父程序Parent process %s'%os.getpid())
            p2=Pool()  
            for name in forum_name:
                p2.apply_async(task2,args=(name,))             
            print ('正等待所有子程序完成 Waiting for all subprocess done ...')
            p2.close()  
            p2.join()  
            print ('所有子程序已經完成 All subprocess done' )
            isnew=0
        time.sleep(600) #10分鐘(600s)自動重爬
