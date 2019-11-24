# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 09:03:36 2019

@author: Harry
"""

#import datetime
#from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
#import csv
#import os.path
import requests
import json

headers = {'Content-Type': "application/json; charset=utf-8"}

class Bapuk:
    storename = ""
    keyword = ""
    kodeunik = ""
    count = 0
    
    def __init__(self,storename):

        print('Start Scrap..')
        keyword = input('Paste the product name here: ')
        REQ = requests.Session()
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        
        for i in range (1,10):
            my_url = "https://www.bukalapak.com/products?utf8=✓&source=navbar&from=omnisearch&page=" + str(i) + "&search_source=omnisearch_organic&from_keyword_history=false&search[hashtag]=&search%5Bkeywords%5D="+keyword
            page_html = REQ.get(my_url,headers=headers)
            #page_html = uClient.read()
            #uClient.close()
            page_soup = BeautifulSoup(page_html.content, 'html.parser')
            #pelapak = page_soup.find("a", {"class":"c-user__name"}).text
            
            containers = page_soup.findAll("div", {"class":"product-card"})
            
            #Open Each Product
            for contain in containers:
                url_produk = "https://www.bukalapak.com" + contain.article.div.a["href"]
                divlapak = contain.find("div", {"class":"user-display-ultra-compact"})
                pelapak = divlapak.select('h5.user__name')[0].text.strip()
                
                if pelapak in storename:
                    print('Get right data..')
                    print('URL = '+url_produk)
                    self.kodeunik = self.getSellerId(url_produk)
                    self.getDetailProduct(self.kodeunik)
                    #print(self.kodeunik)
                    self.count = self.count + 1
                    #self.getDetailProduct(self.kodeunik)
                
        if self.count != 0:
            print('Complete...')
        
    def getSellerId(self,url_produk):
        #get string sampe sebelum jual-
        str1 = url_produk
        str2 = '-jual'
        batas1 = str1.find(str2)
        string1 = str1[0:batas1]
        lenstr = len(string1)
        #get kode uniq barang
        str3 = '/'
        batas2 = string1.rfind(str3)+1
        kode = string1[batas2:lenstr]
        print(kode)
        
        return kode
    
    def getDetailProduct(self,kodeunik):
        REQ = requests.Session()
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        url = 'https://api.bukalapak.com/v2/products/' +kodeunik+ '.json'
        get_data = REQ.get(url,headers=headers)
        get_data = get_data.text
        print(url)
        jsondata = json.loads(get_data)
        #data = get_data.json();
        
        print('Harga = '+str(jsondata['product']['price']))
        print('Grup = '+jsondata['product']['category'])
        #Kategori
        kategori = jsondata['product']['category_structure']
        for val in range(0,len(kategori)):
            print('kategori '+str(val)+' '+kategori[val])
            
        print('Seller = '+jsondata['product']['seller_name'])
        #Gambar
        gambar = jsondata['product']['images']
        for val in range(0,len(gambar)):
            print('Gambar '+str(val)+' '+gambar[val])
            
        print('Stok = '+str(jsondata['product']['stock']))
        
        print('Deskripsi = '+str(jsondata['product']['desc']))
        
        #kurir
        kurir = jsondata['product']['courier']
        for val in range(0,len(kurir)):
            print('Kurir '+str(val)+' '+kurir[val])
        
URL = input('Paste the store name here: ')
Bapuk(URL)