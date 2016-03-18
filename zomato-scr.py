# from lxml import html 
from urllib.request import urlopen
import requests
import json
from bs4 import BeautifulSoup
# from datum import DatumBox
# all_comment=[]
test_url="""
            https://www.zomato.com/bangalore/petoo-yelahanka
            https://www.zomato.com/bangalore/petoo-sarjapur-road
            https://www.zomato.com/FreshMenuIndiranagar/info
            https://www.zomato.com/FreshMenuSarjapur/info
            https://www.zomato.com/FreshMenuJPNagar/info
            https://www.zomato.com/FreshMenuWhitefield/info
            https://www.zomato.com/bangalore/freshmenu-com-kammanahalli/info
            https://www.zomato.com/bangalore/freshmenu-com-marathahalli/info
            https://www.zomato.com/bangalore/freshmenu-com-koramangala-1st-block/info
            https://www.zomato.com/bangalore/freshmenu-com-rajajinagar/info
            https://www.zomato.com/bangalore/freshmenu-com-banashankari/info
            https://www.zomato.com/bangalore/freshmenu-com-electronic-city/info
            https://www.zomato.com/bangalore/freshmenu-com-bannerghatta-road/info
            https://www.zomato.com/bangalore/freshmenu-com-rt-nagar/info
            https://www.zomato.com/bangalore/freshmenu-com-richmond-town/info
            https://www.zomato.com/bangalore/freshmenu-com-frazer-town/info
            https://www.zomato.com/bangalore/freshmenu-com-hsr/info
            https://www.zomato.com/bangalore/freshmenu-com-domlur/info
            https://www.zomato.com/bangalore/freshmenu-com-cv-raman-nagar/info
        """
test_url= test_url.split("\n")
urls=[]
for m in test_url:

    urls.append(m.strip())
# print(urls)
for z in urls:
    if z!="":
        # pass
        class Zomato(object):
            """docstring for Zomato"""
            def __init__(self,url):
                self.url= url
            def get_name(self):pass

            def get_id(self):
                response= urlopen(self.url).read()
                soup=BeautifulSoup(response,"lxml")
                rid= int(soup.find('body')['itemid'])
                return rid
        r= Zomato(z)
        rid=r.get_id()
        print (rid)
        i=0
       
        # FIlter
        # furl="https://www.zomato.com/php/filter_reviews.php"

        while i<100:
            print (i)
            payload={'entity_id':rid,
                    'profile_action':'reviews-dd',
                    'page':i,
                    'limit':5
                    }
                    
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
           
            r= requests.post(url,data= payload,headers= header)
            
            # r2= requests.get(url2)
            new=json.loads(str(r.text))

            # tree = html.fromstring(new['html'])

            soup=BeautifulSoup(new['html'])
            # data = tree.xpath('//div[@class="rev-text"]/text()')
            # print(data)
            # print (s[1])
            # rating=tree.xpath('//div[contains(@class, "ttupper")]')
            data= soup.find_all('div',{'class':'rev-text'})

       
            name=z.replace("/","")
            # print (len(data))
            count=0
            for x in data:
                with open(name,'a+') as f:
                    # i= i.strip("\n",)
                    # print (x)
                    datum= x.find('div').next_sibling.strip()
                    # print (datum)
                    if len(datum)!=0:
                        # pass
                        f.write(datum+"\n")
                        f.write(x.find('div')['aria-label']+"\n")
                        count+=1
            # with open(name,'a+') as d:
            #     d.write(str(rating[i].attrib['aria-label']))           
            # datum= DatumBox
            # d= datum.get_keywords(data)
            if len(data)==0:
                break
            # print(data)
            # all_comment.append(data)
            i+=1
        print(count)
# name=test_url.replace("/","")
# with open(name,'w+') as f:
#     f.write(str(all_comment))
# a= open(test_url,'w+')
# a.write(str(all_comment))
# a.close()
