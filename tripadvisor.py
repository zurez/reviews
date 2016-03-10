from bs4 import BeautifulSoup
from urllib.request import urlopen

class TripAdvisor(object):
	"""docstring for"""
	def __init__(self,url):
		self.url= url
	def last_links(self):
		response= urlopen(self.url).read()
		soup = BeautifulSoup(response)
		links= soup.find_all('a',{'class':'pageNum'})
		return int(links[-1].text)
	def generate_link(self):
		endvalue= self.last_links()
		links=[]
		add= len('Reviews-')
		marker= self.url.index('Reviews-')+add
		for i in range(0,endvalue):
			new_url= self.url[:marker]+"or"+str(i*10)+"-"+self.url[marker:]
			links.append(new_url)
		return links
	def make_call(self):
		links= self.generate_link()
		raw_html=[]
		for i in links:
			raw_html.append(urlopen(i).read())
		return raw_html
	def parse_reviews(self):
		raw_html=self.make_call()
		raw_reviews=[]
		for i in raw_html:
			soup= BeautifulSoup(i)
			raw_reviews.append(soup.find_all('div',{'class':'innerBubble'}))

	def get_reviews(self):
		raw_reviews= self.parse_reviews()
		base_url= "https://www.tripadvisor.in"
		return raw_reviews
		result=[]
		for i in raw_reviews:
			soup=BeautifulSoup(i)
			rating=soup.find('img',{'class':'spritie_rating_sfill'}).get('alt','')
			review_link=base_url+soup.find('div',{'class':'quote'}).find('a',href=True)['href']
			response = urlopen(review_link).read()
			soup = BeautifulSoup(response)
			review= soup.find('p',{'property':'reviewBody'}).text
			result.append((rating,review))
		return result

			



test= TripAdvisor("https://www.tripadvisor.in/Restaurant_Review-g304551-d1417229-Reviews-Indian_Accent-New_Delhi_National_Capital_Territory_of_Delhi.html#REVIEWS")
with open("review_test","wb+") as f:
	for i in test.get_reviews():
		f.write("%s\n" % i)
  # thefile.write("%s\n" % item)
