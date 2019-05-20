# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import json
import pymongo
import slack
import requests

def full_post(item):
    try:
        item_name = item['shoe']['name']
        new_item_photo = item['shoe']['imageUrl']
        new_item_restriction = str(item['shoe']['restricted'])
        new_item_cards = item['shoe']['cards']
        try:
            new_item_price = item['shoe']['product']['price']['msrp']
        except:
            new_item_price = "N/A"
        try:
            new_item_release_type = item['shoe']['product']['selectionEngine']
        except:
            new_item_release_type = "N/A"
        new_item__publish_date = item['shoe']['publishedDate']
        new_item_slug = item['shoe']['seoSlug']
        try:
            new_item_sizes = [s["nikeSize"] for s in item['shoe']['product']['skus']]
        except:
            new_item_sizes = "N/A"
    except Exception as E:
        print(str(E))
    new_sneakers_list = []
    new_sneakers_list = create_field(new_sneakers_list, "Nike Sneakers Monitor(US)", item_name)
    new_sneakers_list = create_field(new_sneakers_list, "Link", "https://www.nike.com/launch/t/" + new_item_slug)
    new_sneakers_list = create_field(new_sneakers_list, "Release Type", new_item_release_type)
    new_sneakers_list = create_field(new_sneakers_list, "Restricted Access", new_item_restriction)
    new_sneakers_list = create_field(new_sneakers_list, "Price", new_item_price)
    if new_item_sizes != 'N/A':
        new_sneakers_list = create_field(new_sneakers_list, "Available Sizes", ', '.join(new_item_sizes))
    else:
        new_sneakers_list = create_field(new_sneakers_list, "Available Sizes", new_item_sizes)
    new_sneakers_list = create_field(new_sneakers_list, "Publish Date", new_item__publish_date)
    attachments = {"thumb_url": new_item_photo, "color": "#bf0000", "fields": new_sneakers_list}
    attachments = [attachments]
    return attachments


def create_field(fieldslist, title, value):
    fieldslist.append({"title": title, "value": value, "short": False})
    return fieldslist


def create_post(item):
    item_name = item['name']
    new_item_photo = item['imageUrl']
    new_item_restriction = str(item['restricted'])
    new_item_cards = item['cards']
    try:
        new_item_price = item['product']['price']['msrp']
    except:
        new_item_price = "N/A"
    try:
        new_item_release_type = item['product']['selectionEngine']
    except:
        new_item_release_type = "N/A"
    new_item__publish_date = item['publishedDate']
    new_item_slug = item['seoSlug']
    try:
        new_item_sizes = [s["localizedSize"] for s in item['product']['skus'] if s["available"]]
        new_item_sizes = "\n".join(new_item_sizes)
    except:
        new_item_sizes = "N/A"
    try:
        style_code = item['product']['style']
    except:
        style_code = "N/A"
    try:
        release_type = item['product']['publishType']
    except:
        release_type = "N/A"
    description = item["seoDescription"]
    new_sneakers_list = []
    new_sneakers_list = create_field(new_sneakers_list, "Link", "https://www.nike.com/launch/t/" + new_item_slug)
    new_sneakers_list = create_field(new_sneakers_list, "Nike Sneakers Monitor(US)", item_name)
    new_sneakers_list = create_field(new_sneakers_list, "Description", description)
    # new_sneakers_list = create_field(new_sneakers_list, "Restricted Access", new_item_restriction)
    # new_sneakers_list = create_field(new_sneakers_list, "Price", new_item_price)
    new_sneakers_list = create_field(new_sneakers_list, "Launch Time", new_item__publish_date)
    new_sneakers_list = create_field(new_sneakers_list, "Launch Type", release_type)
    new_sneakers_list = create_field(new_sneakers_list, "Style Code", style_code)
    new_sneakers_list = create_field(new_sneakers_list, "Size", new_item_sizes)
    attachments = {"thumb_url": new_item_photo, "color": "#bf0000", "fields": new_sneakers_list}
    attachments = [attachments]
    return attachments

class MongoPipeline(object):
    collection_name = "nike"

    def __init__(self, mongo_uri, mongo_db):
        SLACK_TOKEN = "xoxp-640968753094-640968754710-629161756738-b8beada249732e7697a7d5b651d6d20a"
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.slack_client = slack.WebClient(SLACK_TOKEN)

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),

        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    # def process_item(self, item, spider):
    #     ## how to handle each post
    #     try:
    #         results = self.db[self.collection_name].find({'id': item['shoe']['id']})
    #         resultscount = results.limit(1).count()
    #     except Exception as E:
    #         resultscount = 0
    #     if resultscount > 0:
    #
    #         old_item_cards = results[0]['shoe']['cards']
    #         old_item_restriction = results[0]['shoe']['restricted']
    #         old_item_style = results[0]['shoe']['product']['style']
    #         new_item_restriction = item['shoe']['restricted']
    #         new_item_style = item['shoe']['product']['style']
    #         new_item_color = item['shoe']['product']['colorCode']
    #         # if old_item_restriction != new_item_restriction and str(new_item_restriction) == 'true':
    #         #     attachments = full_post(item)
    #         #     self.slack_client.api_call("chat.postMessage", channel="restricted_access", attachments=attachments)
    #         #     print("restricted access!")
    #         # if new_item_style == '999999' and new_item_color == '999' and new_item_style != old_item_style:
    #         #     attachments = full_post(item)
    #         #     self.slack_client.api_call("chat.postMessage", channel="hunt_bet", attachments=attachments)
    #         #     print("hunt_bet")
    #         results = self.db[self.collection_name].update_one({"id": item['shoe']['id']},
    #                                                            item["shoe"], upsert=True)
    #
    #     else:
    #         attachments = full_post(item)
    #         # self.slack_client.api_call("chat.postMessage", channel="new_snkrs", attachments=attachments)
    #         self.db[self.collection_name].insert(dict(item)["shoe"])
    #     logging.debug("Post added to MongoDB")
    #     return item

    def process_item(self, item, spider):
        # results = self.db[self.collection_name].find_one({'id': item['shoe']['id']})
        # if results:
        #     old_item_cards = results['cards']
        #     old_item_restriction = results['restricted']
        #     old_item_style = results['product']['style']
        #     new_item_restriction = item['shoe']['restricted']
        #     new_item_style = item['shoe']['product']['style']
        #     new_item_color = item['shoe']['product']['colorCode']
        add_update = self.db[self.collection_name].replace_one({"id": item['shoe']['id']},
                                                            item["shoe"], upsert=True)
        attachments = create_post(item["shoe"])
        # self.slack_client.chat_postMessage(channel="sneakers", attachments=attachments)
        req_results = requests.post("https://hooks.slack.com/services/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",
                                    json={"attachments": attachments}, headers={'Content-Type': 'application/json'})
        print(req_results.text)
        return item
