#from scrapy.http import HtmlResponse
from random import randint
import pprint
import psycopg2
import re
import traceback
import math,csv
import certifi
import sys
# from datetime import datetime
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError


# dbname="db_config"
# user="postgres"
# host='167.99.127.31'
# password="KenAr@2018"
dbname="data_config_rentacar"
user="postgres"
host='104.236.50.106'
password="WMDRG#020210"

################# Insert config_name into project_config Table #####################
def insert_config(config_name1,proxies):
    config_name = "'{}'".format(config_name1)
    db_structure = "'rent_a_car_template'"
    db_structure_url = "'rent_a_car_1'"
    proxy = "'{}'".format(proxies)
    email_notfification = "NULL"
    db_to_save = "'data_config_rentacar'"
    table_name = "'{}'".format(config_name1)
    server = "'104.236.50.106'"

    TABLE_NAME = "project_config"


    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))
        cur = conn.cursor(cursor_factory=DictCursor)
        # cur.execute("""CREATE TABLE IF NOT EXISTS %s(id serial, name character varying(1000), fields text []) WITH (OIDS=FALSE)"""%TABLE_NAME)
        # conn.commit() 
        cur.execute("insert into "+TABLE_NAME+"(name,db_structure,db_structure_location,proxy,email_notification,db_to_save,table_name,server) values ({},{},{},{},{},{},{},{})".format(config_name,db_structure,db_structure_url,proxy,email_notfification,db_to_save,table_name,server))
        conn.commit()
        # conn.close()
        print("SUCCESSFULLY INSERTED......")
    except Exception as e:
        print("ERROR IN PRO_CONFIG===>",e)
        try:
            conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))
            cur = conn.cursor(cursor_factory=DictCursor)
            # cur.execute("""update """+TABLE_NAME+""" set proxy=%s where name=%s""",(proxy,config_name))
            cur.execute("""update """+TABLE_NAME+""" set proxy={} where name={}""".format(proxy,config_name))
            conn.commit()
            # conn.close()
            print("Proxy SUCCESSFULLY UPDATED")
        except Exception as e:
            print("ERROR 2 ===>",e)

    conn.close()
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)


