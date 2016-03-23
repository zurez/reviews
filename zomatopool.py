import requests
import json
from urllib.request import urlopen

from bs4 import BeautifulSoup
from multiprocessing import Pool
from model import Reviews
"""from 
VARIABLES
"""
header={
    	'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.5',
        'Content-Length':'58',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'PHPSESSID=an57n15lrqu18lrsthhqdef123; fbcity=1; zl=en; fbtrack=ba9e1871dc9a7e04c3c7f8bb4940e794; ueg=1; __utma=141625785.1460912619.1412698053.1412698053.1412698053.1; __utmb=141625785.6.10.1412698053; __utmc=141625785; __utmz=141625785.1412698053.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dpr=1',
        'Host':'www.zomato.com',
        'Referer':'https://www.zomato.com/ncr/fork-you-hauz-khas-village-delhi/reviews',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
        'X-NewRelic-ID':'VgcDUF5SGwEDV1RWAgg=',
        'X-Requested-With':'XMLHttpRequest'
        }
url='https://www.zomato.com/php/social_load_more.php'
class Zomato(object):
	"""docstring for Zomato"""
	def __init__(self,url,survey_id="not provided"):
	    self.url= url
	    self.sid= survey_id
	def get_total(self):pass

	def get_id(self):
	    response= urlopen(self.url).read()
	    soup=BeautifulSoup(response,"lxml")
	    rid= int(soup.find('body')['itemid'])
	    return rid
	def sub_get(self,i):
		rid= self.get_id()
		payload={'entity_id':rid,
		        'profile_action':'reviews-dd',
		        'page':i,
		        'limit':5
		        }
		r= requests.post(url,data= payload,headers= header).text
		response=json.loads(str(r))
		soup=BeautifulSoup(response['html'])
		data= soup.find_all('div',{'class':'rev-text'})
		for x in data:
			review= x.find('div').next_sibling.strip()
			if review!=None or len(review)!=0:
				rating=x.find('div')['aria-label']
				Reviews(provider="zomato",survey_id=self.sid,rating=rating,review=review).save()
	def get_data(self):

		pool= Pool()
		ids=[1,2]
		pool.map(self.sub_get,ids)

test_url="https://www.zomato.com/ncr/alishas-kitchen-aaya-nagar-new-delhi"
z= Zomato(test_url)
z.get_data()

