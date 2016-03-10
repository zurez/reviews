from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
api_base_url="https://developers.zomato.com/api/v2.1/"
api_key="3fae2a3d5cbf4920b04ab01873a03fdb"
class Zomato(object):
	"""docstring for Zomato"""
	def __init__(self,url):
		self.url= url
	def get_id(self):
		response= urlopen(self.url).read()
		soup=BeautifulSoup(response,"lxml")
		rid= int(soup.find('body')['itemid'])
		return rid
	def get_reviews(self):
		api_url= api_base_url+"reviews"
		rid=self.get_id()
		url= api_url+"?res_id="+str(rid)
		header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user-key":api_key}
		response=requests.get(url,headers=header)
		return response.json()

test_url="https://www.zomato.com/ncr/smokeys-bbq-and-grill-dlf-cyber-city-gurgaon"
test= Zomato(test_url)
print (test.get_reviews())

		