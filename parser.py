import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
from shutil import which
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
        
#from selenium.webdriver.chrome.options import Options                                                                                                                                              
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re
import psycopg2
from datetime import datetime
import json
import logging
import requests


def scrape_site(SAMPLE_URL):
    #return 0
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')   
    # options.add_argument('--disable-dev-shm-usage') # Not used but can be an option
    driver = webdriver.Chrome(options=options)

    driver.get(SAMPLE_URL)


    #time.sleep(5)


    #for t in range(10):
    #    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    #for t in range(10):
    #    time.sleep(1)
    #    driver.find_element_by_css_selector('.additional_data').click()

    #src = driver.page_source
    #parser = BeautifulSoup(src, "html.parser")

    result = parse_result(driver,SAMPLE_URL)
    driver.close()

    return result



def load_data(jk,bld,flat_no,square,floor,price,year):
    result = ''
    try:
        headers = {}
        url = "http://api:3000/handle_flat"
        payload = {"jk":jk,"bld":bld,"flat_no":flat_no,"square":square,"floor":floor,"price":price,"year":year}
        s = requests.session()
        s.keep_alive = False
        return requests.request("POST", url, headers=headers, data=payload)

        #connection = psycopg2.connect(user="roman",password="5KNfb^tU9#Zn2ESD",host="db",port="5432",database="postgres")
        #cursor = connection.cursor()
        #cursor.execute("insert into flats  values ('"+jk+"','"+bld+"','"+flat_no+"',"+square+","+floor+","+price+","+str(year)+",'"+str(datetime.now())+"') on CONFLICT(name, building, flat_number)     DO update set price=excluded.price,last_update='"+str(datetime.now())+"';")
        #connection.commit()
    except Exception as error :
        return str(error)
        result +=str(error)+'\n'
        #filename = f'/home/rpolovkov/parklegend/quotes-{page}.html'
        #with open(filename, 'a') as f:
        #    #print ("Error while fetching data from PostgreSQL", error)
        #    f.write("Error while fetching data from PostgreSQL"+ str(error))
    #finally:
        #closing database connection.
        #if (connection):
        #    cursor.close()
        #    connection.close()
    return result
def wait_n_seconds(driver,n):
    try:
        WebDriverWait(driver, n).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "loadMore__100_uH")))
     
    except selenium.common.exceptions.TimeoutException:
        print('1')
def accept_cookies(driver):
    try:           
        cookies = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "accept-cookies")))[0]
        #cookies.find_elements_by_class_name("v3-btn")[0].click()
        ActionChains(driver).move_to_element(cookies.find_element(By.CLASS_NAME,"v3-btn")).click().perform()
    except selenium.common.exceptions.TimeoutException:
        print('1') 
def parse_result(driver, response):
        driver.get(response)
         
        #page="temp"
        #filename = f'/home/rpolovkov/parklegend/quotes-{page}.html'
        element = driver
        number = 0
        number = 0
        i=0
        result = ''
        jk_name = ''
        try:
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*9/10);")
 
            
            i+=1
            wait_n_seconds(driver,8) 
            i+=1
            #accept_cookies(driver) 
            name = WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "nav-title")))
            #return name[0].text
            jk_name = name[0].text
            element = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card")))
 
            for text in element:
                print(text.text)
                print(text.text)
            try:
                while i<3:
                    k=4
                    while k<16 and k>0:
                        try:
                            print(f'i={i}, k={k}')
                            i+=1 
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*"+str(k)+"/15);")
                            
                            wait_n_seconds(driver,2)
                            
                            click_more = driver
                            click_more =  driver.find_element(By.CLASS_NAME,"more-flats-button")
                        
 
                            #click_more.click()
                            
                            after = ActionChains(driver).move_to_element(click_more).click().perform()
                            k+=1
                            print("Next-page")
                            #k=0
                            try:
                                i+=1
                                element = WebDriverWait(print, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flatitem")))
                            except selenium.common.exceptions.TimeoutException:
                                print("Fail")
                                print("TimeoutException")
                                result+='TimeoutException\n'
                            #i+=1

                            wait_n_seconds(driver,2)
                            break
                        except selenium.common.exceptions.MoveTargetOutOfBoundsException:
                            print("Fail")
                            print("MoveTargetOutOfBoundsException")
                            result+='MoveTargetOutOfBoundsException\n'
                            k+=1
                        except Exception as ex:
                            result+=str(ex)+'\n'
                            print('global cycle exception')
                            k+=1
                    i+=1
            except selenium.common.exceptions.MoveTargetOutOfBoundsException:
                print("Fail")
                print("MoveTargetOutOfBoundsException")
                result+='MoveTargetOutOfBoundsException\n'
            except selenium.common.exceptions.NoSuchElementException:
                print("Listed till the end")
                print("NoSuchElementException")
                result+='NoSuchElementException\n'
            except Exception as ex:
                #print (sex))
                print(ex)
                result+=str(ex)+'\n'
            #print(str(response.request.meta['driver'].find_element_by_tag_name("body").get_attribute("text")))
        except selenium.common.exceptions.NoSuchElementException:
            #return ('no title')
            print("Exit")
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card")))
        except selenium.common.exceptions.TimeoutException:
            print("Fail")
            print("TimeoutException")
        for text in element:
            print(text.text)
            link = ""
            try:
                link = str(text.get_attribute("href"))
            except Exception as ex:
                print(f'Exception link: {ex}')
            try:
                text = text.text
                #txt = text.text.replace("\r","")
                #str_ = txt.split("\n")
                #building = str_[1].split('.')
                #flat = str_[4].split(' ')
                #floor = str_[4].split(' ')
                #square = str_[6].split(' ')
                #quart = str_[5].split(' ')
                today = datetime.today()
                lines = text.split('\n')
                second = lines[2].split(',')
                bld = ""
                try:
                    bld = f'{second[0]}, {second[1]}'
                except Exception as ex:
                    print(f'Building parse error: {ex}')
                print(bld)
                flat_no = ""
                try:
                    flat_no = second[3].strip() + link
                    print(flat_no)
                except Exception as ex:
                    print(f'Flat parse error: {ex}')
                square = ""
                try:
                    square = lines[1].split('м')[0]
                except Exception as ex:
                    print(f'Square parse error: {ex}')
                print(square)
                floor = ""
                try:
                    floor  = second[2].split(' ')[1]
                except Exception as ex:
                    print(f'Floor parse error: {ex}')
                print(floor)
                i = 4
                size = len(lines)
                while i<size:
                    p_price = lines[i].replace(' ','')
                    if p_price[0]<'9' and p_price[0]>'0':
                        break
                    i+=1
                price = lines[i].replace(' ','').replace('¤','').replace('₽','')
                print(price)
                year = 0
                ready = lines[3].split(' ')
                if len(ready)==1:
                    year = today.year
                else:
                    year = ready[2]
                print(year)
                result += f'{jk_name}, {bld}, {flat_no}, {square}, {floor}, {price}, {year} \n'
                print(f'{jk_name}, {bld}, {flat_no}, {square}, {floor}, {price}, {year} \n' )
                result += str(load_data(jk_name,bld,flat_no,square,floor,price,year))
                #load_data(jk_name,str_[2]+' '+str_[3].replace(',',''),str_[0]+' '+str(text.get_attribute("href")),square[0],floor[1],str_[7].replace(' ','').replace('¤',''),quart[2])
            except Exception as ex:
                print("Exception"+str(ex))
        return result

