import pymongo
from pymongo import MongoClient
import csv
import os
import json
import pandas as pd

# header for csv file
header = ["source_file", "created_at", "retweeted_status_created_at", "tweet_id", "tweet_text",
                     "user_id", "user_name", "user_screen_name", "user_location",
                     "user_time_zone", "user_lang", "coordinates", "place_bounding_box",
                     "place_country_code", "place_country", "place_full_name",
                     "place_name", "hashtags", "media_url_https", "extended_url_type", "type", "lang",
                     "retweeted_status_tweet_id",
                     "retweeted_status_user_screen_name", "tweet_link"]

result_dir = "/media/"
source_dir = "/media//"
original_download_file_list = os.listdir(source_dir)
if not os.path.exists(result_dir):
    os.makedirs(result_dir)


def import_content(s_dir, r_dir, count_dup):
    with open(s_dir, 'r') as f, open(r_dir, 'a') as f_out:
        try:
            # reads the tweets from file
            reader = csv.DictReader((x.replace('\0', '') for x in f), fieldnames=header)
            # writes tweets to file
            writer = csv.DictWriter(f_out, fieldnames=header, extrasaction='ignore')
            # write the header to file
            writer.writeheader()
            # skips the header while reading the file
            next(reader)
            coll.create_index("original_tweet_id", name='index', background=True, unique=True)
            for row in reader:
                # data = pd.read_csv('9-28-2017_english_filtered.csv')
                # payload = json.loads(data.to_json(orient='records'))
                #         coll.remove()
                try:
                    # only keep it if you want to read without duplicate tweets
                    # remove it if you want to preserve retweets
                    original_tweet_id = row['retweeted_status_tweet_id'] if row['retweeted_status_tweet_id'] != ' ' else row['tweet_id']
                    row['original_tweet_id'] = original_tweet_id

                    # inserts data in collection
                    coll.insert(row)
                    # writes tweets to file if duplicate not found
                    writer.writerow(row)
                except pymongo.errors.DuplicateKeyError:
                    count_dup += 1
                    print('duplicate found', count_dup)
                    continue

        except Exception as e:
            print(e)


if __name__ == '__main__':
    # starting mongodb client
    client = MongoClient('127.0.0.1', 27017)
    # creates new database
    db = client['CSV_db']
    # creates mongodb collection inside the database
    coll = db['tab_name']
    # removes existing documents from the collection before reading data in collection
    # comment this out if you want to preserve the data that already exists
    # coll.remove()
    count_dup = 0
    for filename in original_download_file_list:
        filename = os.path.splitext(filename)[0]
        source_path = source_dir + filename + '.csv'
        result_path = result_dir + 'noDuplicates.csv'
        import_content(source_path, result_path, count_dup)
    print coll.count()
