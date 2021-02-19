from selenium import webdriver
from lxml.html import fromstring, tostring
from time import strftime
import argparse
import datetime
import multiprocessing
import random
import re
import sqlite3
import sys
import time
import traceback
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import datetime
import os
from pyvirtualdisplay import Display
import psycopg2
import smtplib
import random
import signal
import traceback
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# sys.path.append("/root/BHRUK/cfiles")
from func import *
from pro_config import *
# sys.path.insert(1, '/root/automate_sites/')
# from send_email import *
import PIL
from PIL import Image
from time import gmtime, strftime
import logging as logging1,logging
print(strftime("%z", gmtime()))
d = Display(visible=0, size=(1378,786))
d.start()

def getText(parsed_source, xpath_str):
    try:
        text = parsed_source.xpath(xpath_str)
        if len(text) == 0:
            return ''
        else:
            return text[0].replace('\n','').replace('\t','').replace('\r','').strip()
    except:
        return ""

def validateDate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

now  = datetime.datetime.now()
now = now.strftime("%Y-%m-%d")
# print(now)
date_1 = datetime.datetime.strptime(str(now), "%Y-%m-%d")
extraction_date = date_1 + datetime.timedelta(days=int(sys.argv[1]))
extraction_date = extraction_date.strftime("%Y-%m-%d")
print(extraction_date)
if validateDate(extraction_date) is True:

    day_limits = [1,7,28]
    for day in day_limits:
        no_weekend = False

        hours = datetime.timedelta(hours=12)
        days = datetime.timedelta(days=day)

        pickUpDate = datetime.datetime.strptime(extraction_date, '%Y-%m-%d') + hours
        dropOfDate = pickUpDate + days

        if (pickUpDate.isoweekday() != 6) or (pickUpDate.isoweekday() != 7):
            if (dropOfDate.isoweekday() != 6) or (dropOfDate.isoweekday() != 7):
                no_weekend = True
                
        if no_weekend is False:
            message = ("Wrong Days: pickUpDate (%s) / dropOfDate (%s) ... day limits (%s)" % (pickUpDate.strftime("%A"), dropOfDate.strftime("%A"), day))
            print(message)
            sys.exit()
else:
    print('Error: Wrong format of Pick up Date. use YYYY-MM-DD')
    sys.exit()
config_name_1= str(sys.argv[2]) #name in project_config
config_name=config_name_1+'_'+pickUpDate.strftime("%Y%m%d")
config_type = str(sys.argv[3])
proxies = 'torguard'
insert_config(config_name,proxies)
project_configs = get_my_project_config(config_name,config_type)
if project_configs:
    proxy_handler = get_proxy_details(project_configs[3])
    db_variable = project_configs[8]
    print(db_variable)
    table_name = project_configs[6]
    db_user_pass = get_db_details(project_configs[7])
else:
    print("Something went wrong with project config !!")
    sys.exit()
if config_type != 'data': tb_name = '{}_location'.format(table_name)
else: tb_name = table_name

for n, val in enumerate(db_variable):
        listOfGlobals = globals()
        globals()[val] = ''

LOG_FILENAME = '/root/BHRUK/racewaysnet/racewaysnet_'+pickUpDate.strftime("%Y%m%d")+'.log'
error_filename='/root/BHRUK/racewaysnet/racewaysnet_error_'+pickUpDate.strftime("%Y%m%d")+'.log'
listOfGlobals['Fromdate']=pickUpDate.strftime("%Y-%m-%d %H:%M").replace('12:00','00:00:00')
# logging.basicConfig(filename="\\root\\common_framwork\\raceways\\abc.log") 
fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(ch)
logger.addHandler(fh)
#----------------error log
fh1 = logging1.FileHandler(error_filename)
fh1.setLevel(logging1.INFO)
ch1 = logging1.StreamHandler()
ch1.setLevel(logging1.DEBUG)
formatter1 = logging1.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch1.setFormatter(formatter1)
fh1.setFormatter(formatter1)
logger1 = logging1.getLogger('errorlog')
logger1.setLevel(logging1.INFO)
logger1.addHandler(ch1)
logger1.addHandler(fh1)
screenshotFolder ='/root/BHRUK/racewaysnet/racewaysnet_'+pickUpDate.strftime("%Y%m%d")+'/' ##'./racewaysnet_'+pickUpDate.strftime("%Y%m%d")+'/'
if not os.path.exists(screenshotFolder):
    os.mkdir(screenshotFolder)
#browser = webdriver.PhantomJS()



website_name='www.raceways.net'
created_date=str(now)
pickup_date2=str(pickUpDate.strftime("%Y-%m-%d"))
log_file_name='racewaysnet_'+pickUpDate.strftime("%Y%m%d")+'.log'
log_file_path='/root/BHRUK/racewaysnet/'
log_details(db_user_pass,created_date,pickup_date2,log_file_name,log_file_path,website_name)

job_name=config_name
status=1
# pickup_date1=str(pickUpDate.strftime("%Y-%m-%d"))
created_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
completed_date=''
error_log=str('racewaysnet_error_'+pickUpDate.strftime("%Y%m%d")+'.log')
spider_jobs(db_user_pass,website_name,job_name,status,pickup_date2,completed_date,created_date,error_log)
try:
    browser = webdriver.Firefox()
    browser.maximize_window()
except Exception as E:
    status='2'
    completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_spider_jobs(db_user_pass,job_name,status,completed_date)
    print(E)
    print('browser not open')
    logger1.exception(traceback.print_exc())
nextPage = "https://www.raceways.net/rentals/"
logger.info("getting:{}".format(nextPage))
bikes = set()

while nextPage is not None:
    print(nextPage)

    try:
        browser.get(nextPage)
        time.sleep(5)
        html = fromstring(browser.page_source)
    except Exception as E:
        status='2'
        completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
        print(E)
        print('Get bikes urls FAILED')
        # logger.exception(traceback.print_exc())
        logger1.info("error for:{}".format(nextPage))
        logger1.exception(traceback.print_exc())
        browser.quit()

    bikeUrls = html.xpath('//div[@class="product-view"]/a/@href')
    for bikeUrl in bikeUrls:
        bikes.add(bikeUrl)

    try:
        nextPage = html.xpath('//li[@class="bpn-next-link"]/a/@href')[0]
    except:
        nextPage = None
        logger1.info("error for:{}".format(nextPage))
        logger1.exception(traceback.print_exc())
        break

print("total bikes: ", len(bikes))
count = 1

pickup_date = datetime.datetime.strptime(pickUpDate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
day_1 = datetime.timedelta(days=1)
dropof_date_1 = pickup_date+day_1
day_7 = datetime.timedelta(days=7)
dropof_date_7 = pickup_date+day_7

for bikeUrl in bikes:
    print ("getting data for: ", bikeUrl)
    logger.info("getting bike url:{}".format(bikeUrl))
    browser.get(bikeUrl)
    logger.info("got bike url:{}".format(bikeUrl))
    scrapeInfo = {

        'source': 'www.raceways.net',
        'day_limits': 'N/A',
        'locationUrl': bikeUrl,
        'locationName': '',
        'pickUpDate': pickup_date.strftime("%Y-%m-%d %H:%M"),
        'dropOfDate_1': dropof_date_1.strftime("%Y-%m-%d %H:%M"),
        'dropOfDate_7': dropof_date_7.strftime("%Y-%m-%d %H:%M"),
        'transmission': 'N/A',
        'screenshotName': 'N/A',
        'Vehicletype': 'N/A',
        'Category': 'N/A',
        'Make': 'N/A',
        'Model': 'N/A',
        'Prepay_1': 'N/A',
        'Prepay_7': 'N/A',
        'Payoncollection': 'N/A',
        'locationCode': '',

        }

    html = fromstring(browser.page_source)

    try:
        prepay_1 = html.xpath('//div[@class="col-md-5"]/div[2]/div[1]/text()')[0][1:]#col-md-5
        scrapeInfo['Prepay_1'] = prepay_1
        logger.info("prepay 1 :{}".format(prepay_1))
    except Exception as E:
        prepay_1='N/A'
        scrapeInfo['Prepay_1'] = prepay_1
        status='2'
        completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
        print (E)
        # logger.exception(traceback.print_exc())
        logger1.info("error for:{}".format(bikeUrl))
        logger1.exception(traceback.print_exc())
        pass

    try:
        prepay_7 = html.xpath('//div[@class="col-md-5"]/div[2]/div[3]/text()')[0][1:]
        scrapeInfo['Prepay_7'] = prepay_7
        logger.info("prepay 7 :{}".format(prepay_7))
    except Exception as E:
        status='2'
        completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
        print (E)
        # logger.exception(traceback.print_exc())
        logger1.info("error for:{}".format(bikeUrl))
        logger1.exception(traceback.print_exc())
    
    print ("prepay_1:",prepay_1,"prepay_7",prepay_7)
    

    try:
        make = html.xpath('//table[@class="table details-table"]/tbody/tr[1]/td[2]/text()')[0]
        scrapeInfo['Make'] = make
        scrapeInfo['Make'] = scrapeInfo['Make'].replace("HONDA","Honda")
    except Exception as E:
        status='2'
        completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
        print (E)
        # logger.exception(traceback.print_exc())
        logger1.info("error for:{}".format(bikeUrl))
        logger1.exception(traceback.print_exc())
    scrapeInfo['locationName'] = 'SE16 2LW'
    try:
        # model = html.xpath('//table[@class="table details-table"]/tbody/tr[2]/td[2]/text()')[0]
        model = html.xpath("//h1/text()")[0]
        model = model.replace(make,'').strip()
        scrapeInfo['Model'] = model 
        scrapeInfo['Model'] = scrapeInfo['Model'].replace('Honda','').strip()    
    except Exception as E:
        status='2'
        completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
        print(E)
        # logger.exception(traceback.print_exc()) 
        logger1.info("error for:{}".format(bikeUrl))
        logger1.exception(traceback.print_exc())
    if "Keeway" in make:
        make = 'Benelli'
        model = model.replace('Benelli','Keeway')
        scrapeInfo['Make'] = make
        scrapeInfo['Model'] = model
    logger.info("make and model:{},{}".format(make,model))  
    try:
        cc = html.xpath('//table[@class="table details-table"]/tbody/tr[3]/td[2]/text()')[0]
        age = html.xpath('//table[@class="table details-table"]/tbody/tr[4]/td[2]/text()')[0]

        Vehicletype = ("CC %s; MIN. AGE %s" % (cc, age))
        scrapeInfo['Vehicletype'] = Vehicletype
        logger.info("vhivletype is :{}".format(Vehicletype))      
    except Exception as E:
        status='2'
        completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
        print (E)
        # logger.exception(traceback.print_exc())
        logger1.info("error for:{}".format(bikeUrl))
        logger1.exception(traceback.print_exc())

    try:
        screenshotDate = pickup_date.strftime("%m-%Y")
        scrapeInfo['screenshotName'] = ("%s_%s.jpg" % (bikeUrl.split('/')[-2], screenshotDate))
        print ("saving screenshot")
        total_width = browser.execute_script("return document.body.offsetWidth")
        total_height = browser.execute_script("return document.body.parentNode.scrollHeight")
        print(1270,total_height)
        browser.set_window_size(1270,total_height)
        browser.save_screenshot('testing.jpg')
        print("screenshot saved=================================>")
        image = Image.open("testing.jpg")
        image = image.convert('RGB')
        basewidth, hsize = image.size
        img = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save(screenshotFolder + scrapeInfo['screenshotName'])
        logger.info("schreenshot is done  :{}".format(scrapeInfo['screenshotName']))
        # browser.save_screenshot(screenshotFolder + scrapeInfo['screenshotName'])
        
        print ("saving",scrapeInfo)
        listOfGlobals['Todate']=dropof_date_1.strftime("%Y-%m-%d %H:%M").replace('12:00','00:00:00')
        listOfGlobals['Make']=scrapeInfo['Make']
        listOfGlobals['Model']=scrapeInfo['Model']
        listOfGlobals['Source']='www.raceways.net'
        listOfGlobals['Company']='raceways'
        listOfGlobals['Location']='SE16 2LW'
        listOfGlobals['Vehicletype']=scrapeInfo['Vehicletype']
        listOfGlobals['Category']='N/A'
        listOfGlobals['Transmission']='N/A'
        listOfGlobals['Prepay']=prepay_1
        listOfGlobals['Payoncoll']='N/A'
        listOfGlobals['Screenshot']=scrapeInfo['screenshotName']
        listOfGlobals['Excess1']='N/A'
        listOfGlobals['Cdw1']='N/A'
        listOfGlobals['Excess2']='N/A'
        listOfGlobals['Cdw2']='N/A'
        listOfGlobals['Excess3']='N/A'
        listOfGlobals['Cdw3']='N/A'
        input_columns = [listOfGlobals[x] for x in db_variable ]
        print(input_columns)
        logger.info("1day data is done  :{}".format(input_columns))
        insert_db(db_user_pass,tb_name,input_columns,db_variable)
        listOfGlobals['Todate']=dropof_date_7.strftime("%Y-%m-%d %H:%M").replace('12:00','00:00:00')
        listOfGlobals['Prepay']=prepay_7
        listOfGlobals['Screenshot']=scrapeInfo['screenshotName']
        input_columns = [listOfGlobals[x] for x in db_variable ]
        print(input_columns)
        logger.info("7day data is done  :{}".format(input_columns))
        logger.info('***************************')
        insert_db(db_user_pass,tb_name,input_columns,db_variable)
        print ("remaining cars",len(bikeUrls)-count)
        count+=1
    except Exception as E:
        status='1'
        completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_spider_jobs(db_user_pass,job_name,status,completed_date)
        print (E)
        # logger.exception(traceback.print_exc())
        logger1.info("error for:{}".format(bikeUrl))
        logger1.exception(traceback.print_exc())
status='3'
completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
update_spider_jobs(db_user_pass,job_name,status,completed_date)
# send_email(extraction_date,"racewaysnet_"+extraction_date+" completed","racewaysnet_"+extraction_date+" completed")
browser.quit()
d.stop()
