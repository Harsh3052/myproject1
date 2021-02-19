import sys
import random
import psycopg2
from lxml.html import fromstring, tostring
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError
import sys, requests, random, json
from random import randint
import sys
sys.path.append("/root")
try:
    from industryparts.config.browser_fingerPrint  import *
except:
    sys.path.append("/root/industryparts/config")
    from browser_fingerPrint import *
from scrapy.http import HtmlResponse
from multiprocessing import Process, Pool
# from googletrans import Translator
import os
from bs4 import BeautifulSoup
import json

proxy_handler = {}
# config_dbname="db_config"
# config_user="postgres"
# # config_host="173.249.56.73"
# config_host='167.99.127.31'
# config_password="KenAr@2018"
# config_password='tyres@123'
config_dbname="data_config_rentacar"
config_user="postgres"
# config_host="173.249.56.73"
config_host='104.236.50.106'
config_password="WMDRG#020210"

# core_count=os.cpu_count()
########## Create Data Table  ###########################
def create_data_table(db_structure,save_db,tb_name,ip_address,db_structure_url):
    res = get_table_template(db_structure,'data')
    get_db_creds = get_db_details(ip_address)
    table_fields = []
    if res:
        print("Using {} Template for creating table {}".format(db_structure,tb_name))
        # print(res)
        for x in res[2].split(','):
            table_fields.append('{} text'.format(x))
        if get_db_creds:
            dbname=save_db
            conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,get_db_creds[1],get_db_creds[0],get_db_creds[2]))
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute("""CREATE TABLE IF NOT EXISTS {} ( id serial, {} ) WITH (OIDS=FALSE)""".format(tb_name,','.join(table_fields)))
            conn.commit()
            conn.close()
            print('Data Table Created [If not Exist]')
        else:
            print('Unable to fetch the server credentials. Check server details in db_details table.!!')
    else:
        print("Unable to find a table structure in DB !!")
        sys.exit()
    return table_fields

########## Create URL Table  ###########################
def create_url_table(db_structure,save_db,tb_name,ip_address,db_structure_url):
    res = get_table_template(db_structure_url,'url')
    get_db_creds = get_db_details(ip_address)
    table_fields = []
    if res:
        print("Using {} URL Template for creating table {}".format(db_structure_url,tb_name))
        for x in res[2].split(','):
            if x == 'scrapped':
                table_fields.append('{}  integer'.format(x))
            # elif x == 'scraped':
            #     table_fields.append('{} boolean'.format(x))
            else:
                table_fields.append('{} text'.format(x))
        print("TABLE FIELDS",table_fields)
        print("TABLE FIELDS=====>",','.join(table_fields))
        if get_db_creds:
            dbname=save_db
            conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,get_db_creds[1],get_db_creds[0],get_db_creds[2]))
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute("""CREATE TABLE IF NOT EXISTS {}_location ( id serial, {} ) WITH (OIDS=FALSE)""".format(tb_name,','.join(table_fields)))
            conn.commit()
            conn.close()
            print('Url Table Created [If not Exist]')
        else:
            print('Unable to fetch the server credentials. Check server details in db_details table.!!')
            sys.exit()
    else:
        print("Unable to find a table structure in DB !!")
        sys.exit()
    return table_fields

    
########## Call URL and DATA creating Methods and Return Columns Variables ###########################
def get_my_project_config(project_name,table_type):
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,config_user,config_host,config_password))
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("select * from project_config where name='{}'".format(project_name))
    res = cur.fetchone()
    data = []
    if res:
        if table_type == 'data':
            data = create_data_table(res[1],res[5],res[6],res[7],res[2])
            data = [x.split(' ')[0].strip() for x in data]
        elif table_type == 'url':
            data = create_url_table(res[1],res[5],res[6],res[7],res[2])
            print("DATA 1",data)
            data = [x.split(' ')[0].strip() for x in data]
            print("DATA 2",data)
        else:
            print("Please mention the table type data/url in the get_my_project_config function")
    else:
        print("No configruation available in the db for this project => {}".format(project_name))
        sys.exit()
    res.append(data)
    return res

########## Get All Data from Url and Data Table  ###########################
def get_table_template(db_structure,d_u):
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,config_user,config_host,config_password))
    cur = conn.cursor(cursor_factory=DictCursor)
    if d_u == "data":
        cur.execute("select * from db_structures where name='{}'".format(db_structure))
    if d_u == "url":
        cur.execute("select * from db_structures_location where name='{}'".format(db_structure))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

########## Get Database Information  ###########################
def get_db_details(ip_address):
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,config_user,config_host,config_password))
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("select * from db_details where ip_address='{}'".format(ip_address))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

########## Get Proxy Information  ###########################
def get_proxy_details(name):
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,config_user,config_host,config_password))
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("select * from proxy where name='{}'".format(name))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    if  len(res)==1:
        res1 = res[0]
        print(res1)
        res= {
                "http": "http://{}:{}@{}:{}".format(res1[2],res1[3],res1[4],res1[5]),
                "https": "https://{}:{}@{}:{}".format(res1[2],res1[3],res1[4],res1[5])
            }
    else:
        print('*******Enter In Multiple Choice proxy*******')
        domain = []
        if  res:
            for row in res:
                domain.append(row[4])
            myProxy= random.choice(domain)
            res1 = res[0]
            res =  {'host': myProxy, 'port': res1[5], 'usr': res1[2], 'pwd': res1[3]}
            print(res)
        else:
            print('Unable to find the specified proxy')
            sys.exit()
    return res


########################## Inserting in to DB #################
def insert_db(db_user_pass,tb_name,input_columns,db_variable):
    try:
        z = str("%"+"s")
        for i in range(1,len(db_variable)):
                    z += str(","+"%"+"s")
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
        cur = conn.cursor(cursor_factory=DictCursor)
        #insert_url = ''' INSERT INTO {}({}) VALUES({})''' .format(tb_name,','.join(db_variable),','.join(input_columns))
        cur.execute("insert into "+tb_name+" values (DEFAULT,"+z+")", input_columns)
        conn.commit()
        conn.close()
        print("DATA SUCCESSFULLY INSERTED...........")
    except Exception as ex:
        print(ex)
        pass
########################## Update Scraped in to DB #################
def update_db(db_user_pass,tb_name,product_url,colum_name,day_limits):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute("update "+tb_name+"_location set scrapped='1' where "+colum_name+"=%s and day_limits=%s",(product_url,day_limits))
        conn.commit()
        conn.close()
        print("DATA SUCCESSFULLY UPDATED")
    except Exception as ex:
        print(ex)
        pass
    
########################## Fetch all Url where scraped='False' ################
def get_productURLS(db_user_pass,tb_name):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute("select product_url from {}_product_urls where scraped='False'  order by id asc;".format(tb_name))
        res = cur.fetchall()
        conn.commit()
        conn.close()
        print("Inserted")
    except Exception as ex:
        pass
    return res

########################## Define Headers ################
def get_headers():
    li = randint(3, 9) / 10
    lj = randint(3, 9) / 10
    accept_lang = 'en-{}; q={}, en; q={}'.format('en', li, lj)
    extra_amount = 25
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=' \
            + str(lj) + ',image/webp,image/apng,*/*;q=' \
            + str(lj) \
            + ',application/signed-exchange;v=b3;q=' \
            + str(lj) + '',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': accept_lang,
        'Connection': 'keep-alive',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(user_agent_list),
        }
    return headers

########################## This Method returns the response of the Url ################
def get_page_response(session,url,postmethod,data,headers,proxy_handler):
            try:
                if postmethod == "get":
                        return_response=session.get(url, proxies=proxy_handler,headers=headers)
                if postmethod == "post":
                        return_response=session.post(url, proxies=proxy_handler,headers=headers,data=data)
            except Exception as ex:
                print(ex)
                pass
            return {'session': session, 'return_response' : return_response}

def get_scrapy_response (response):
    return  HtmlResponse(url="my HTML string", body=response.text, encoding='utf-8')


def get_bs4_response (response):
    return  BeautifulSoup(response.content, 'html.parser')

def get_lxml_response(response):
    return BeautifulSoup(response.text,'lxml')

# def get_weekly_data()
def get_location(db_user_pass,tb_name,colum_name):
    # try:
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("select "+colum_name+",day_limits from {}_location where scrapped='0'  order by id asc;".format(tb_name))
        # print(cur.execute("select "+colum_name+",day_limits from {}_queue where scrapped='0'  order by id asc;".format(tb_name)))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    print("Inserted")
    # except Exception as ex:
    #     pass
    return res

def from_queue_locations(db_user_pass,tb_name):
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
    cur = conn.cursor(cursor_factory=DictCursor)
    tb_name=tb_name.split('_')[0]
    cur.execute("select * from "+tb_name+"_location")
    res=cur.fetchall()
    conn.commit()
    conn.close()
    return res
def get_proxy():
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,config_user,config_host,config_password))
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("select * from proxy")
    res = cur.fetchall()
    # print(res)
    conn.commit()
    conn.close()
    return res
def log_details(db_user_pass,created_date,pickup_date,log_file_name,log_file_path,website_name):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
        cur = conn.cursor(cursor_factory=DictCursor)
        # cur.execute("select log_file_name,pickup_date from log_details")
        cur.execute("select log_file_name,pickup_date from log_details where log_file_name='{}' and pickup_date='{}' and created_date='{}'".format(log_file_name,pickup_date,created_date))
        res=cur.fetchall()
            #insert_url = ''' INSERT INTO {}({}) VALUES({})''' .format(tb_name,','.join(db_variable),','.join(input_columns))
        if len(res)==0:
            cur.execute("insert into log_details (id,created_date,pickup_date,log_file_name,log_file_path,website_name) values (DEFAULT,%s,%s,%s,%s,%s)",(created_date,pickup_date,log_file_name,log_file_path,website_name))
            conn.commit()
            conn.close()
            print("LOG SUCCESSFULLY INSERTED...........")
        else:
            cur.execute("update log_details set log_file_name=%s where log_file_name=%s and pickup_date=%s and created_date=%s" ,(log_file_name,log_file_name,pickup_date,created_date))
            conn.commit()
            conn.close()
            print("LOG SUCCESSFULLY UPDATED...........spider")
    except Exception as ex:
        print(ex)
        # print(traceback.print_exc())
        pass
def spider_jobs(db_user_pass,website_name,job_name,status,pickup_date,completed_date,created_date,error_log):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
        cur = conn.cursor(cursor_factory=DictCursor)
            #insert_url = ''' INSERT INTO {}({}) VALUES({})''' .format(tb_name,','.join(db_variable),','.join(input_columns))
        cur.execute("select job_name from spider_jobs")
        res=cur.fetchall()
        # print(res)
        # print(job_name)
        job=[]
        for i in range(0,len(res)):
            job.append(res[i][0])
        if job_name in job:
            cur.execute("update spider_jobs set status=%s ,pickup_date=%s where job_name=%s" ,(status,pickup_date,job_name))
            conn.commit()
            conn.close()
            print("DATA SUCCESSFULLY UPDATED...........spider")
        else:
            data = None
            cur.execute("insert into spider_jobs (id,website_name,job_name,status,pickup_date,completed_date,created_date,error_log,tab,instinct,jtab) values (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(website_name,job_name,status,pickup_date,completed_date,created_date,error_log,None,None,None))
            conn.commit()
            conn.close()
            print(" DATA SUCCESSFULLY INSERTED...........spider")
    except Exception as ex:
        print(ex)
        # print(traceback.print_exc())
        pass
def update_spider_jobs(db_user_pass,job_name,status,completed_date):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute("update spider_jobs set status=%s ,completed_date=%s where job_name=%s" ,(status,completed_date,job_name))
        conn.commit()
        conn.close()
        print("DATA SUCCESSFULLY UPDATED spider")
    except Exception as ex:
        print(ex)
        pass

def tab_spider_jobs(db_user_pass,website_name,job_name,status,pickup_date,completed_date,created_date,error_log,tab,instinct):
    if int(tab) == 1:
        spider_jobs(db_user_pass,website_name,job_name,status,pickup_date,completed_date,created_date,error_log)
    else:
        try:
            conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
            cur = conn.cursor(cursor_factory=DictCursor)
                #insert_url = ''' INSERT INTO {}({}) VALUES({})''' .format(tb_name,','.join(db_variable),','.join(input_columns))
            # cur.execute("select * from tab_spider_jobs")
            cur.execute("select job_name,tab,instinct from spider_jobs where job_name='{}' and tab='{}'".format(job_name,tab))
            res=cur.fetchall()
            # print(job_name)
            print(res)
            if len(res)==0:
                tabs = tab
                tabs_dic = {}
                for i in range(1,(tabs+1)):
                    tabs_dic[i] = 1
                tabs_dic[instinct]=status
                print(tabs_dic)
                tabs_dic = json.dumps(tabs_dic)
                cur.execute("insert into spider_jobs (id,website_name,job_name,status,pickup_date,completed_date,created_date,error_log,tab,instinct,jtab) values (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(website_name,job_name,status,pickup_date,completed_date,created_date,error_log,tab,instinct,tabs_dic))
                conn.commit()
                conn.close()
                print("***************** TAB DATA SUCCESSFULLY INSERTED...........spider")
            else:
                cur.execute("select jtab from spider_jobs where job_name='{}' and tab='{}'".format(job_name,tab))
                res=cur.fetchone()
                tabs_dic = res[0]
                tabs_dic[str(instinct)]=status
                print(tabs_dic)
                tabs_dic = json.dumps(tabs_dic)
                cur.execute("update spider_jobs set status=%s ,completed_date=%s , jtab=%s where job_name=%s and tab=%s" ,(status,completed_date,tabs_dic,job_name,tab))
                conn.commit()
                conn.close()
                print("***************** TAB DATA SUCCESSFULLY UPDATED...........spider")
            # job=[]
            # for i in range(0,len(res)):
            #     job.append(res[i][0])
            # if job_name in job:
            #     cur.execute("update tab_spider_jobs set status=%s ,pickup_date=%s where job_name=%s" ,(status,pickup_date,job_name))
            #     conn.commit()
            #     conn.close()
            #     print("DATA SUCCESSFULLY UPDATED...........spider")
            # else:
            #     cur.execute("insert into tab_spider_jobs (id,website_name,job_name,status,pickup_date,completed_date,created_date,error_log,tab,instinct) values (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(website_name,job_name,status,pickup_date,completed_date,created_date,error_log,tab,instinct))
            #     conn.commit()
            #     conn.close()
            #     print("***************** TAB DATA SUCCESSFULLY INSERTED...........spider")
        except Exception as ex:
            print(ex)
            # print(traceback.print_exc())
            pass
def tab_update_spider_jobs(db_user_pass,job_name,status,completed_date,tab,instinct):
    if int(tab) == 1:
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
    else:
        try:
            conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute("select jtab from spider_jobs where job_name='{}' and tab='{}'".format(job_name,tab))
            res=cur.fetchone()
            tabs_dic = res[0]
            print(tabs_dic)
            tabs_dic[str(instinct)]=status
            print(tabs_dic)
            tabs_dic = json.dumps(tabs_dic)
            cur.execute("update spider_jobs set status=%s ,completed_date=%s , jtab=%s where job_name=%s and tab=%s" ,(status,completed_date,tabs_dic,job_name,tab))
            conn.commit()
            # conn.close()
            print("***************** TAB DATA SUCCESSFULLY UPDATED.*******************spider")
            cur.execute("select jtab from spider_jobs where job_name='{}' and tab='{}' ".format(job_name,tab))
            res=cur.fetchone()
            tabs_dic = res[0]
            print(type(tabs_dic))
            state_3 = []
            state_2 = []
            job=list(tabs_dic.values())
            print(job)
            for i in job:
                if i==str(3):
                    state_3.append(i)
                if i==str(2):
                    state_2.append(i)
            print(state_3)
            if len(state_3) == int(tab):
                cur.execute("update spider_jobs set status=3 ,completed_date=%s  where job_name=%s and tab=%s" ,(completed_date,job_name,tab))
                conn.commit()
                # conn.close()
                print("TASK SUCCESSFULLY COMPLETED?????????????")
            if len(state_2) >= int(1):
                cur.execute("update spider_jobs set status=2 ,completed_date=%s where job_name=%s and tab=%s" ,(completed_date,job_name,tab))
                conn.commit()
                # conn.close()
                print("ERROR OCCURED IN SCRIPT!!!!!!!!!!!!!!!!!!!!!")
            #     cur.execute("delete from tabjson_spider_jobs where job_name=%s and tab=%s and status='3' and instinct!='1' " ,(job_name,tab))
            conn.commit()
            conn.close()
            # else:
            #     for i in range(0,len(res)):
            #         if int(res[i][0])== 2:
            #             # job.append(res[i][0])
            #             cur.execute("delete from tabjson_spider_jobs where job_name=%s and tab=%s and status='3' or status='2' and instinct!=%s " ,(job_name,tab,res[i][2]))
            #             conn.commit()
            #             conn.close()

        except Exception as ex:
            print(ex)
            pass

def insert_db_duplicates_remove(db_user_pass,tb_name,input_columns,db_variable,column_name,prepay,prepay_value,location,location_value):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
        cur = conn.cursor(cursor_factory=DictCursor)   
        # cur.execute("select * from "+tb_name)
        cur.execute("select {} from {} where {}='{}' and {}='{}'".format(column_name,tb_name,prepay,prepay_value,location,location_value))
        res = cur.fetchall()
        print(res)
        conn.commit()
        conn.rollback()
        conn.close()
        try:
            if len(res)==0:
                z = str("%"+"s")
                for i in range(1,len(db_variable)):
                            z += str(","+"%"+"s")
                try:
                    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
                    cur = conn.cursor(cursor_factory=DictCursor)
                    #insert_url = ''' INSERT INTO {}({}) VALUES({})''' .format(tb_name,','.join(db_variable),','.join(input_columns))
                    cur.execute("insert into "+tb_name+" values (DEFAULT,"+z+")", input_columns)
                    conn.commit()
                    # conn.close()
                    print("DATA SUCCESSFULLY INSERTED...........")
                except IntegrityError:
                        conn.rollback()
                except Exception as e:
                        print(e)
                        conn.rollback()
                conn.close()
                # conn2.close()
                del input_columns 
            else:
                print("Duplicate Item found")
            # else:
            #     # for row in res:
            #     if input_columns in res:
            #         pass
            #     else:
            #         z = str("%"+"s")
            #         for i in range(1,len(db_variable)):
            #                     z += str(","+"%"+"s")
            #         conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(config_dbname,db_user_pass[1],db_user_pass[0],db_user_pass[2]))
            #         cur = conn.cursor(cursor_factory=DictCursor)
            #         #insert_url = ''' INSERT INTO {}({}) VALUES({})''' .format(tb_name,','.join(db_variable),','.join(input_columns))
            #         cur.execute("insert into "+tb_name+" values (DEFAULT,"+z+")", input_columns)
            #         conn.commit()
            #         conn.close()
            #         print("DATA SUCCESSFULLY INSERTED...........")
        except Exception as ex:
            print(ex)
    except Exception as ex:
        print(ex)
        pass