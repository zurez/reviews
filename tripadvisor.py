from bs4 import BeautifulSoup
from urllib.request import urlopen
# import ssl
# from functools import wraps
# def sslwrap(func):
#     @wraps(func)
#     def bar(*args, **kw):
#         kw['ssl_version'] = ssl.PROTOCOL_TLSv1
#         return func(*args, **kw)
#     return bar

# ssl.wrap_socket = sslwrap(ssl.wrap_socket)
class TripAdvisor(object):
	"""docstring for"""
	def __init__(self,url):
		self.url= url
	def last_links(self):
		response= urlopen(self.url).read()
		soup = BeautifulSoup(response)
		links= soup.find_all('a',{'class':'pageNum'})
		# return links
		try:
			return int(links[-1].text)
		except Exception as e:
			return 1
		
	def generate_link(self):
		endvalue= self.last_links()
		links=[self.url]
		if endvalue==1:
			return links
			
		
		add= len('Reviews-')
		marker= self.url.index('Reviews-')+add
		for i in range(1,endvalue):
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
		return raw_reviews

	def get_reviews(self):
		raw_reviews= self.parse_reviews()
		base_url= "https://www.tripadvisor.in"
		# return raw_reviews
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

			


test_url="https://www.tripadvisor.in/Restaurant_Review-g1162523-d4009998-Reviews-The_Beer_Cafe-Kirtinagar_Uttarakhand.html"
test= TripAdvisor(test_url)
# print (test.get_reviews())
with open("review_test","wb+") as f:
	for i in test.get_reviews():
		f.write("%s\n" % i)
  # thefile.write("%s\n" % item)
