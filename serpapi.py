import requests
import scrapy
import pandas as pd

file_path = "Greendeck Business Analyst Assignment Task 4 - Sheet1.csv"
df = pd.read_csv(file_path)
df['query'] = df['Google Search Code'].apply(lambda x: 'site:oneill.com/fr ' + '"' + x + '"')

def create_products_dic(x):
	products.append({
        'product_price': 0,
        'product_code': x,
        'product_url': 0,
        'product_query': df[df['Google Search Code'] == x]['query'].item()
    })

products = []
df['Google Search Code'].apply(create_products_dic)

for product in products:
	params = {
        "access_key": "3a6ef3c8063ecc7b45241f340b506280",
        "query": product['product_query'],
		"gl": "fr",
		"location": "france",
	}
	api_result = requests.get("http://api.serpstack.com/search", params)
	api_response = api_result.json()
	if len(api_response["organic_results"]) > 0:
		product['product_url'] = api_response["organic_results"][0]["url"]
	else:
		product['product_url'] = "no_url_response_from_api"

class BlueTomatoSpider(scrapy.Spider):
	name = "serp_api"
	# allowed_domains = ["http://www.oneill.com/"]

	def start_requests(self):
		for product in products:
			if(product['product_url'] != "no_url_response_from_api"):
				yield scrapy.Request(product['product_url'], callback=self.parse, cb_kwargs=dict(product_code = product['product_code']))
			else:
				product['product_price'] = 'no_url_to_scrape_price'
	
	def parse(self, response, product_code):
		price = response.xpath(
			"//div[@class='product__asset product-price-and-badge-wrapper']/div[@class='product-price-wrapper']/span[@class='product-price product-price--sale']/text()"
			).get()
		if price is not None:
			price = price.replace('€', '')
		self.log(price)
		for i in products:
			if(i['product_code'] == product_code):
				i['product_price'] = price
			self.log(products)