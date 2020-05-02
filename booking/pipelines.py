import sqlite3
from .items import HotelItem, HotelInfoItem, HotelRoomItem, HotelReviewItem

class BookingPipeline:
    def __init__(self):
            self.create_connection()
            self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("hotels.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS hotel_table""")
        self.curr.execute("""DROP TABLE IF EXISTS hotel_info_table""")
        self.curr.execute("""DROP TABLE IF EXISTS hotel_room_table""")
        self.curr.execute("""DROP TABLE IF EXISTS hotel_review_table""")
        self.curr.execute("""create table hotel_table(
                    id text,
                    name text,
                    star text,
                    link text,
                    coordinate text,
                    image_url text,
                    price text,
                    hotelid_fk,
                    page text
                    )""")
        self.curr.execute("""create table hotel_info_table(
                    id text,
                    name text,
                    star text,
                    link text,
                    coordinate text,
                    image_url text,
                    price text
                    )""")
        self.curr.execute("""create table hotel_room_table(
                    id text,
                    sleeps text,
                    room_type text,
                    bed_type text,
                    size text,
                    hotelid_fk text
                    )""")
        self.curr.execute("""create table hotel_review_table(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name text,
                    country text,
                    rate text,
                    date text,
                    title text,
                    positive_content text,
                    negative_content text,
                    hotelreview_fk text
                    )""")
        # self.curr.execute("""insert into hotel_review_table values(9223372036854775807,'Test','test','test','test','test','test','test','test')""")

    def process_item(self, item, spider):
        if isinstance(item, HotelItem):
            self.store_hotel(item)
        if isinstance(item, HotelInfoItem):
            self.store_hotel_info(item)
        if isinstance(item, HotelRoomItem):
            self.store_room_info(item)
        if isinstance(item, HotelReviewItem):
            self.store_hotel_review(item)
        return item

    def store_hotel(self, item):
        self.curr.execute("""insert into hotel_table values (?,?,?,?,?,?,?,?,?)""",(
            item['id'],
            item['name'],
            item['star'],
            item['link'],
            item['coordinate'],
            item['image_url'],
            item['price'],
            item['hotelid_fk'],
            item['page']
        ))
        self.conn.commit()

    def store_hotel_info(self, item):
        self.curr.execute("""insert into hotel_info_table values (?,?,?,?,?,?,?)""",(
            item['id'],
            item['rate'],
            item['address'],
            item['description'],
            item['joined_date'],
            item['property_type'],
            item['review_count'],
        ))
        self.conn.commit()

    def store_room_info(self, item):
        self.curr.execute("""insert into hotel_room_table values (?,?,?,?,?,?)""",(
            item['id'],
            item['sleeps'],
            item['room_type'],
            item['bed_type'],
            item['size'],
            item['hotelroomid_fk'],
        ))
        self.conn.commit()

    def store_hotel_review(self, item):
        self.curr.execute("""insert into hotel_review_table values (?,?,?,?,?,?,?,?,?)""",(
            None,
            item['name'],
            item['country'],
            item['rate'],
            item['date'],
            item['title'],
            item['positive_content'],
            item['negative_content'],
            item['hotelreview_fk'],
        ))
        self.conn.commit()
