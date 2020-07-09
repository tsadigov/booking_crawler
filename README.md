# booking_crawler
Scrapy project to crawl hotel info from booking.com

1. Configure scrapy environment on your computer as shown in given url - https://docs.scrapy.org/en/latest/intro/tutorial.html
2. Clone the repository 
3. Then open booking.com to search for hotels in any country
4. After the search, go to the second page
5. Copy the last url, delete the offset of the page and paste in booking_spider.py
6. Change 'desired_count_to_scrape' to the desired number (I recommend you to take at least 5 more than the result number of pages)
7. Open 'cmd'
8. Go to the project directory, where you cloned the repo
9. Type: scrapy crawl booking
10. Enter
11. As a result, all data will be collected in booking_hotels.db in 3 tables (my crawl for hotels in Azerbaijan is given as an example in the repo)

Note: After this, crawler will run and you will see items data shown simultaneously in your terminal
