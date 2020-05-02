import scrapy

class HotelItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    star = scrapy.Field()
    link = scrapy.Field()
    coordinate = scrapy.Field()
    image_url = scrapy.Field()
    price = scrapy.Field()
    hotelid_fk = scrapy.Field()
    page = scrapy.Field()

class HotelInfoItem(scrapy.Item):
    id = scrapy.Field()
    rate = scrapy.Field()
    address = scrapy.Field()
    description = scrapy.Field()
    joined_date = scrapy.Field()
    property_type = scrapy.Field()
    review_count = scrapy.Field()

class HotelRoomItem(scrapy.Item):
    id = scrapy.Field()
    sleeps = scrapy.Field()
    room_type = scrapy.Field()
    bed_type = scrapy.Field()
    size = scrapy.Field()
    hotelroomid_fk = scrapy.Field()

class HotelReviewItem(scrapy.Item):
    # id = scrapy.Field()
    name = scrapy.Field()
    country = scrapy.Field()
    rate = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    positive_content = scrapy.Field()
    negative_content = scrapy.Field()
    hotelreview_fk = scrapy.Field()
