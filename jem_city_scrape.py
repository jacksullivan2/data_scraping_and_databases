from bs4 import BeautifulSoup
import requests 
import mysql.connector 

db = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='TigerWoods06!',
		database='jem_city')

my_cursor = db.cursor()
# Created the products table in the jem_city database. So, I've commented out this code. 
# my_cursor.execute("CREATE TABLE products (item VARCHAR(40), price VARCHAR(15), image_url VARCHAR(180) PRIMARY KEY)")


web_pages = ['https://www.jemcityuk.shop/collections/all', 'https://www.jemcityuk.shop/collections/all?page=2',
		'https://www.jemcityuk.shop/collections/all?page=3']

for web_page in web_pages:

	source = requests.get(web_page).text
	soup = BeautifulSoup(source, 'lxml')
	
	for article in soup.find_all('div', class_='grid__item small--one-half medium-up--one-fifth'):

		name = article.find('div', class_='product-card__name').text
		print(name)

		try:
			price = article.find('span', class_='money').text
		except AttributeError:
			price = 'Sold Out'
	
		print(price)
		
		image = article.find('img', class_="product-card__image")['src']
		image_url = f"https:{image}"
		print(image_url)

		# Load data into the database table #
		query = "INSERT INTO products(item, price, image_url) VALUES (%s,%s,%s)"
		values = (name, price, image_url)
		
		my_cursor.execute(query, values)
		db.commit()

		print()


