# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    
    base_url = 'https://www.redfin.com/city/11203/CA/Los-Angeles'
    
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    try:
       os.remove('redfin1.csv')
    except OSError:
       pass   
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }

    # general crawler
    def start_requests(self):
       
            # initial HTTP request
            yield scrapy.Request(
                url=base_url,
                headers=self.headers,
               
                callback=self.parse
            )
            
    def  parse(self,response):     
           
         content = ''
         with open('redfin.html', 'r' ) as f:
             for line in f.read():
                 content += line
         response = Selector(text=content)
             
         properties = [script for script in response.css('script').getall() if '<script type="application/ld+json">' in script]
         for prop in properties:
           prop = prop.split('<script type="application/ld+json">')[-1]
           prop=prop.split('</script>')[0]
           
          
           prop = json.loads(prop)
           prop2 = json.dumps(prop, indent = 2)
           #print(prop2, '\n\n')
           for data in prop:
               if isinstance(data, dict):
                   features =  {
                       'Name' : data['name'],
                       'Url' : data['url'],
                       'Address' : data.get('address', ''),

                       
                   }
                   print(features)
           
              
            
    
# main driver
if __name__ == '__main__':
    # run scraper
#    process = CrawlerProcess()
#    process.crawl(ResidentialSale)
#    process.start()
    
     ResidentialSale.parse(ResidentialSale, '')
    
    
