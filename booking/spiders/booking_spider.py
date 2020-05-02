import scrapy
import re, math
from scrapy.loader import ItemLoader
from booking.items import HotelItem, HotelInfoItem, HotelRoomItem, HotelReviewItem
import sys, os


class BookingSpider(scrapy.Spider):
    name = "booking"

    months = ['January','February','March','December']
    hotel_id_list = []
    page_offset = 0
    list_prev_len = 0
    list_cur_len = 0
    count = 0

    url = "https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaBGIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AuaN7PMFwAIB&sid=1ec3a7e834ccaaaf9cd6ac22cb6dedd4&tmpl=searchresults&ac_click_type=b&ac_position=0&class_interval=1&dest_id=15&dest_type=country&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=country&room1=A&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&srpvid=389233fc26a90038&ss=Azerbaijan&ss_all=0&ss_raw=Azerbaijan&ssb=empty&sshis=0&top_ufis=1&rows=25&offset="

    def start_requests(self):
        yield scrapy.Request(self.url+"0", self.parse)

    #for every hotel
    def parse(self, response):

        items = HotelItem()

        hotels = response.css('div.sr_item')
        print("Page Count ----- >>> ", self.count)
        self.count += 1

        for hotel in hotels:

            if hotel.attrib['data-hotelid'] not in self.hotel_id_list:
                items['id'] = hotel.attrib['data-hotelid']
                items['name'] = hotel.css('span.sr-hotel__name::text').get().strip()
                temp_star = hotel.css('i.bk-icon-stars::attr(title)').get()
                if temp_star is not None:
                    items['star'] = temp_star[0]
                else:
                    items['star'] = "No Star"
                items['link'] = "https://www.booking.com" + hotel.css('a.hotel_name_link::attr(href)').get().strip()
                items['coordinate'] = hotel.css('a.bui-link::attr(data-coords)').get().strip()
                items['image_url'] = hotel.css('img.hotel_image::attr(data-highres)').get().strip()
                items['price'] = "No price yet"
                items['hotelid_fk'] = self.get_id(items['link'])#items['link']
                self.hotel_id_list.append(items['id'])
                print(self.count," -------------------------------------------------------------- ")
                # print(self.hotel_id_list)
                items['page'] = str(self.count)
                yield items

                yield scrapy.Request(items['link'], callback = self.parse_hotel_info)

        self.list_cur_len = len(self.hotel_id_list)
        self.page_offset+=25

        # if self.list_prev_len != self.list_cur_len:
        if self.count < 60:
            self.list_prev_len = self.list_cur_len
            next_page = self.url + str(self.page_offset)
            yield scrapy.Request(next_page, self.parse)

    def parse_hotel_info(self, response):

        items = HotelInfoItem()
        items['id'] = self.get_id(response.request.url)#response1.request.url
        items['rate'] = response.css('div.bui-review-score__badge::text').get()
        # items['address'] = self.check_empty(response1.css('span.hp_address_subtitle::text').get())
        items['address'] = response.css('span.hp_address_subtitle::text').get()

        '''Handle description list'''
        items['description'] = ''
        r = response.css('div#property_description_content')
        description_list = r.css('p::text').getall()
        for list in description_list:
            items['description'] += list
        '''-----------------'''
        items['joined_date'] = response.css('span.hp-desc-highlighted::text').get().split("since")[1][1:-2]
        hotel_name_tag = response.css('h2#hp_hotel_name')
        items['property_type'] = hotel_name_tag.css('span::text').get()

        reviews_tab = response.css('a#show_reviews_tab').css('span::text').getall()
        if len(reviews_tab) > 1:
            items['review_count'] = re.split('[()]',reviews_tab[1])[1]
        else:
            items['review_count'] = "0"

        yield items

        '''Handle roomd info here'''
        items1 = HotelRoomItem()
        #
        table = response.css('table.roomstable')
        body = table.css('tbody')
        rows = body.css("tr")
        #
        for row in rows:
            sleeps = row.css("span.bui-u-sr-only::text").get()
            roomtype = row.css("a.jqrt::text").getall()
            bed = row.css("td.roomType")
            roominfo = row.css("div.room-info")

            if sleeps:
                s = ""
                beds = bed.css("li")
                for b in beds:
                    b1 = b.css("strong::text").get()
                    b2 = b.css("span::text").get().strip()
                    s += (b1.strip() if b1 else "") + " " + b2 + "#"

                items1['id'] = roominfo.attrib['id'][2:]
                items1['sleeps'] = sleeps
                items1['room_type'] = roomtype[1].strip()
                items1['bed_type'] = s.strip()
                items1['size'] = 'no size yet'
                items1['hotelroomid_fk'] = items['id']

                yield items1
        # url = "https://www.booking.com/reviewlist.html?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaBGIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Aobe6e8FwAIB;cc1=az;dist=1;pagename="+items['id']+";srpvid=7f8e530322ea0011;type=total&;offset="+str(0)+";rows=10"
        url = "https://www.booking.com/reviewlist.html?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaBGIAQGYASG4ARfIAQzYAQHoAQH4AQuIAgGoAgO4ArbIqPMFwAIB;sid=3643ba2153d911b23ec5137c20672813;cc1=az;dist=1;srpvid=57695460816d0019;type=total&;rows=10;pagename=" + items['id'] + ";offset=0;review_count=" + items['review_count']
        yield scrapy.Request(url, callback=self.parse_reviews)

    def parse_reviews(self,response):

        item2 = HotelReviewItem()

        forUrl = response.request.url.split("0;review_count=")
        print(forUrl)
        url = forUrl[0]
        review_count = self.str_to_int(forUrl[1])
        pagename = url.split("pagename=")[1].split(";offset")[0]
        offset = int(url.split("offset=")[1]+ "0")
        flag = 1
        blocks = response.css("li.review_list_new_item_block")

        for b in blocks:
            name = b.css("span.bui-avatar-block__title::text").get().strip()
            country = b.css("span.bui-avatar-block__subtitle::text").get()
            rate = b.css("div.bui-review-score__badge::text").get()
            date = b.css('div.c-review-block__row').css("span.c-review-block__date::text").get().split(":")[1].strip()

            r_title = self.check_empty(b.css("h3.c-review-block__title::text").get())
            reviews = b.css("div.c-review__row")

            month = date.split(" ")[1]
            year = date.split(" ")[2]
            if (month in self.months) and (int(year) >= 2019):
                item2['name'] = name
                item2['country'] = country
                item2['rate'] = rate
                item2['date'] = date
                item2['title'] = r_title
                item2['positive_content'] = ''
                item2['negative_content'] = ''
                for review in reviews:
                    if review.css('span.bui-u-sr-only::text').get() == 'Liked':
                        item2['positive_content'] = review.css('span.c-review__body::text').get()
                    if review.css('span.bui-u-sr-only::text').get() == 'Disliked':
                        item2['negative_content'] = review.css('span.c-review__body::text').get()

                item2['hotelreview_fk'] = pagename
                yield item2

            else:
                flag = 0
                break

        offset += 10

        if (review_count >= offset) and flag:
            yield scrapy.Request(url.split("offset=")[0]+ "offset=" + str(offset) + ";review_count=" + str(review_count), self.parse_reviews)

    def str_to_int(self, number):
        number = number.split(",")
        num = ""
        for n in number:
            num += n
        return int(num)

    def get_id(self,url):
        url_list = url.split("/")
        page_name = url_list[-1].split(".")[0]
        return page_name

    def check_empty(self, value):
        if value:
            return value.strip()
        else:
            return ""
