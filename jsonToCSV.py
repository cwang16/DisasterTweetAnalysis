import json
import os, io
import csv
import demjson

# source directory with json file
# notice: in the end of the path, there is backslash needed
source_dir = "/media/"
original_download_file_list = os.listdir(source_dir)
# result directory
result_dir = "/media/"
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

total_json = 0
parsed_csv = 0
parsed_csv_smart = 0
invalid_json = 0

def generate_csv (input_data):
    urls = []
    types = []
    video_types = []
    write_to_csv = []

    screen_name = ""
    id_str =""
    # get entities media url and type
    if "extended_tweet" not in data and "retweeted_status" not in data and "quoted_status" not in data:  # tweet only
        if "extended_entities" in data and data["extended_entities"] is not None and "media" in data["extended_entities"] \
                and data["extended_entities"]["media"] is not None:
            for media in data["extended_entities"]["media"]:
                if "video_info" in media:
                    for v in media["video_info"]["variants"]:
                        urls.append(v["url"])
                        types.append(media["type"])
                        video_types.append((v["content_type"]))
                else:
                    urls.append(media["media_url_https"])
                    types.append(media["type"])
        if "entities" in data and data["entities"] is not None and "media" in data["entities"] and \
                        data["entities"]["media"] is not None:
            for media in data["entities"]["media"]:
                if len(types) == 0 and len(urls) == 0:
                    if "video_info" in media:
                        for v in media["video_info"]["variants"]:
                            urls.append(v["url"])
                            types.append(media["type"])
                            video_types.append((v["content_type"]))
                    else:
                        urls.append(media["media_url_https"])
                        types.append(media["type"])

    elif "extended_tweet" in data and "retweeted_status" not in data and "quoted_status" not in data:  # extended_tweet only
        if "entities" in data["extended_tweet"] and data["extended_tweet"]["entities"] is not None \
                and "media" in data["extended_tweet"]["entities"] and \
                        data["extended_tweet"]["entities"]["media"] is not None:
            for media in data["extended_tweet"]["entities"]["media"]:
                if "video_info" in media:
                    for v in media["video_info"]["variants"]:
                        urls.append(v["url"])
                        types.append(media["type"])
                        video_types.append((v["content_type"]))
                else:
                    urls.append(media["media_url_https"])
                    types.append(media["type"])
        if "entities" in data["extended_tweet"] and data["extended_tweet"]["entities"] is not None \
                and "media" in data["extended_tweet"]["entities"] and \
                        data["extended_tweet"]["entities"]["media"] is not None:
            if len(types) == 0 and len(urls) == 0:
                for media in data["extended_tweet"]["entities"]["media"]:
                    if "video_info" in media:
                        for v in media["video_info"]["variants"]:
                            urls.append(v["url"])
                            types.append(media["type"])
                            video_types.append((v["content_type"]))
                    else:
                        urls.append(media["media_url_https"])
                        types.append(media["type"])
    elif "retweeted_status" in data and "quoted_status" not in data:  # retweet only
        if "extended_tweet" not in data["retweeted_status"]:
            if "extended_entities" in data["retweeted_status"] \
                    and "media" in data["retweeted_status"]["extended_entities"] \
                    and data["retweeted_status"]["extended_entities"]["media"] is not None:
                for media in data["retweeted_status"]["extended_entities"]["media"]:
                    if "video_info" in media:
                        for v in media["video_info"]["variants"]:
                            urls.append(v["url"])
                            types.append(media["type"])
                            video_types.append((v["content_type"]))
                    else:
                        urls.append(media["media_url_https"])
                        types.append(media["type"])
            elif "entities" in data["retweeted_status"] \
                    and "media" in data["retweeted_status"]["entities"] \
                    and data["retweeted_status"]["entities"]["media"] is not None:
                for media in data["retweeted_status"]["entities"]["media"]:
                    if len(types) == 0 and len(urls) == 0:
                        if "video_info" in media:
                            for v in media["video_info"]["variants"]:
                                urls.append(v["url"])
                                types.append(media["type"])
                                video_types.append((v["content_type"]))
                        else:
                            urls.append(media["media_url_https"])
                            types.append(media["type"])
        elif "extended_tweet" in data["retweeted_status"]:
            if "extended_entities" in data["retweeted_status"]["extended_tweet"] \
                    and data["retweeted_status"]["extended_tweet"]["extended_entities"] is not None\
                    and "media" in data["retweeted_status"]["extended_tweet"]["extended_entities"]\
                    and data["retweeted_status"]["extended_tweet"]["extended_entities"]["media"] is not None:
                for media in data["retweeted_status"]["extended_tweet"]["extended_entities"]["media"]:
                    if "video_info" in media:
                        for v in media["video_info"]["variants"]:
                            urls.append(v["url"])
                            types.append(media["type"])
                            video_types.append((v["content_type"]))
                    else:
                        urls.append(media["media_url_https"])
                        types.append(media["type"])
            elif "entities" in data["retweeted_status"]["extended_tweet"] \
                    and data["retweeted_status"]["extended_tweet"]["entities"] is not None\
                    and "media" in data["retweeted_status"]["extended_tweet"]["entities"]\
                    and data["retweeted_status"]["extended_tweet"]["entities"]["media"] is not None:
                for media in data["retweeted_status"]["extended_tweet"]["entities"]["media"]:
                    if len(types) == 0 and len(urls) == 0:
                        if "video_info" in media:
                            for v in media["video_info"]["variants"]:
                                urls.append(v["url"])
                                types.append(media["type"])
                                video_types.append((v["content_type"]))
                        else:
                            urls.append(media["media_url_https"])
                            types.append(media["type"])
    elif "quoted_status" in data:
        if "extended_tweet" not in data["quoted_status"]:
            if "extended_entities" in data["quoted_status"] \
                    and "media" in data["quoted_status"]["extended_entities"] \
                    and data["quoted_status"]["extended_entities"]["media"] is not None:
                for media in data["quoted_status"]["extended_entities"]["media"]:
                    if "video_info" in media:
                        for v in media["video_info"]["variants"]:
                            urls.append(v["url"])
                            types.append(media["type"])
                            video_types.append((v["content_type"]))
                    else:
                        urls.append(media["media_url_https"])
                        types.append(media["type"])
            elif "entities" in data["quoted_status"] \
                    and "media" in data["quoted_status"]["entities"] \
                    and data["quoted_status"]["entities"]["media"] is not None:
                for media in data["quoted_status"]["entities"]["media"]:
                    if len(types) == 0 and len(urls) == 0:
                        if "video_info" in media:
                            for v in media["video_info"]["variants"]:
                                urls.append(v["url"])
                                types.append(media["type"])
                                video_types.append((v["content_type"]))
                        else:
                            urls.append(media["media_url_https"])
                            types.append(media["type"])
        elif "extended_tweet" in data["quoted_status"]:
            if "extended_entities" in data["quoted_status"]["extended_tweet"] \
                    and data["quoted_status"]["extended_tweet"]["extended_entities"] is not None\
                    and "media" in data["quoted_status"]["extended_tweet"]["extended_entities"]\
                    and data["quoted_status"]["extended_tweet"]["extended_entities"]["media"] is not None:
                for media in data["quoted_status"]["extended_tweet"]["extended_entities"]["media"]:
                    if "video_info" in media:
                        for v in media["video_info"]["variants"]:
                            urls.append(v["url"])
                            types.append(media["type"])
                            video_types.append((v["content_type"]))
                    else:
                        urls.append(media["media_url_https"])
                        types.append(media["type"])
            elif "entities" in data["quoted_status"]["extended_tweet"] \
                    and data["quoted_status"]["extended_tweet"]["entities"] is not None\
                    and "media" in data["quoted_status"]["extended_tweet"]["entities"]\
                    and data["quoted_status"]["extended_tweet"]["entities"]["media"] is not None:
                for media in data["quoted_status"]["extended_tweet"]["entities"]["media"]:
                    if len(types) == 0 and len(urls) == 0:
                        if "video_info" in media:
                            for v in media["video_info"]["variants"]:
                                urls.append(v["url"])
                                types.append(media["type"])
                                video_types.append((v["content_type"]))
                        else:
                            urls.append(media["media_url_https"])
                            types.append(media["type"])

    # Start to write the first column of CSV
    # A source_file
    write_to_csv.append(filename +".json")
    # B create_at ---- create time of the tweet (can be the retweet/quote tweet created time,
    # or if it is tweet only , it will be the tweet created time)
    if "created_at" in data:
        write_to_csv.append(data["created_at"])
    else:
        write_to_csv.append(" ")
    # C retweeted_status_created_at ---- the original time, including the original tweet from
    # retweet or quoted tweet. To keep consistent with all files, the filed name is "retweeted_stats_created_at..."
    # in fact, if the tweet is quoted tweet, this field will be the original tweet info from quoted tweet
    if "retweeted_status" in data and "quoted_status" not in data: # meaning this is retweet only
        if data["retweeted_status"] is not None:
            if data["retweeted_status"]["created_at"] is not None:
                write_to_csv.append(data["retweeted_status"]["created_at"])
    elif "quoted_status" in data and "retweeted_status" not in data:
        if data["quoted_status"] is not None:
            if data["quoted_status"]["created_at"] is not None:
                write_to_csv.append(data["quoted_status"]["created_at"])
    elif "retweeted_status" in data and "quoted_status" in data: # meaning this is retweet with quote tweet
        if data["quoted_status"] is not None:
            if data["quoted_status"]["created_at"] is not None:
                write_to_csv.append(data["quoted_status"]["created_at"])
    else:
        write_to_csv.append(" ")
    # D tweet_id
    # It is useful only the tweet is tweet only or tweet+extended_tweet only
    # It is useless when the current record is retweet or quoted tweet as it is not original tweet id.
    # The original tweet id (id in retweeted_status or quoted_status) is saved in "retweeted_status_tweet_id"
    if "id_str" in data:
        write_to_csv.append(data["id_str"])
    else:
        write_to_csv.append(" ")
    # E tweet_text
    # this is the original tweet longest text
    if "extended_tweet" not in data and "retweeted_status" not in data and "quoted_status" not in data:# tweet only
        write_to_csv.append(data["text"].encode('utf-8'))
    elif "extended_tweet" in data and "retweeted_status" not in data and "quoted_status" not in data:# extended_tweet only
        if "full_text" in data["extended_tweet"]:
            write_to_csv.append(data["extended_tweet"]["full_text"].encode('utf-8'))
        else:
            write_to_csv.append(" ")
    elif "retweeted_status" in data and "quoted_status" not in data: #retweet only
        if "extended_tweet" not in data["retweeted_status"]:
            write_to_csv.append(data["retweeted_status"]["text"].encode('utf-8'))
        elif "extended_tweet" in data["retweeted_status"]:
            write_to_csv.append(data["retweeted_status"]["extended_tweet"]["full_text"].encode('utf-8'))
    elif "quoted_status" in data:
        if "extended_tweet" not in data["quoted_status"]:
            write_to_csv.append(data["quoted_status"]["text"].encode('utf-8'))
        elif "extended_tweet" in data["quoted_status"]:
            write_to_csv.append(data["quoted_status"]["extended_tweet"]["full_text"].encode('utf-8'))
    else:
        print "E Tweet_text can't found in: ", input_data
    # F user_id
    # useless as it is not the original tweet id
    if "user" in data and "id" in data["user"]:
        write_to_csv.append(data["user"]["id"])
    else:
        write_to_csv.append(" ")
    # G user_name
    # useless as it is not original author name
    if "user" in data and "name" in data["user"]:
        write_to_csv.append(data["user"]["name"].encode("utf-8"))
    else:
        write_to_csv.append(" ")
    # H user_screenname
    # useless as it is not original author
    if "user" in data and "screen_name" in data["user"]:
        write_to_csv.append(data["user"]["screen_name"])

    else:
        write_to_csv.append(" ")
    # I user_location
    # useless as it is not original author
    if "user" in data:
        if "location" in data["user"]:
            if data["user"]["location"] is not None:
                write_to_csv.append(data["user"]["location"].encode("utf-8"))
            else:
                write_to_csv.append(" ")
        else:
            write_to_csv.append(" ")
    else:
        write_to_csv.append(" ")

    # J user_time_zone
    if "user" in data and "time_zone" in data["user"]:
        write_to_csv.append(data["user"]["time_zone"])
    else:
        write_to_csv.append(" ")

    # K user_lang
    if "user" in data and "lang" in data["user"]:
        write_to_csv.append(data["user"]["lang"])

    # L Coordinate
    if "extended_tweet" not in data and "retweeted_status" not in data and "quoted_status" not in data:# tweet only
        if "coordinates" in data and data["coordinates"] is not None and "coordinates" in data["coordinates"]:
            write_to_csv.append(data["coordinates"]["coordinates"])
        else:
            write_to_csv.append(" ")
    elif "extended_tweet" in data and "retweeted_status" not in data and "quoted_status" not in data:# extended_tweet only
        if "coordinates" in data and data["coordinates"] is not None and "coordinates" in data["coordinates"]:
            write_to_csv.append(data["coordinates"]["coordinates"])
        else:
            write_to_csv.append(" ")
    elif "retweeted_status" in data and "quoted_status" not in data: #retweet only
        if "coordinates" in data["retweeted_status"] and data["retweeted_status"]["coordinates"] is not None \
                and "coordinates" in data["retweeted_status"]["coordinates"]:
            write_to_csv.append(data["retweeted_status"]["coordinates"]["coordinates"])
        else:
            write_to_csv.append(" ")
    elif "quoted_status" in data:
        if "coordinates" in data["quoted_status"] and data["quoted_status"]["coordinates"] is not None \
                and "coordinates" in data["quoted_status"]["coordinates"]:
            write_to_csv.append(data["quoted_status"]["coordinates"]["coordinates"])
        else:
            write_to_csv.append(" ")
    else:
        write_to_csv.append(" ")
        print "E Coordinates can't found in: ", input_data

    # M place_bounding_box
    if "extended_tweet" not in data and "retweeted_status" not in data and "quoted_status" not in data:# tweet only
        if "place" in data and data["place"] is not None and data["place"]["bounding_box"] is not None and \
                        data["place"]["bounding_box"]["coordinates"] is not None:
            write_to_csv.append(data["place"]["bounding_box"]["coordinates"])
        else:
            write_to_csv.append(" ")
    elif "extended_tweet" in data and "retweeted_status" not in data and "quoted_status" not in data:# extended_tweet only
        if "place" in data and data["place"] is not None and data["place"]["bounding_box"] is not None and \
                        data["place"]["bounding_box"]["coordinates"] is not None:
            write_to_csv.append(data["place"]["bounding_box"]["coordinates"])
        else:
            write_to_csv.append(" ")
    elif "retweeted_status" in data and "quoted_status" not in data: #retweet only
        if "place" in data["retweeted_status"] and data["retweeted_status"]["place"] is not None and \
                        data["retweeted_status"]["place"]["bounding_box"] is not None and \
                        data["retweeted_status"]["place"]["bounding_box"]["coordinates"] is not None:
            write_to_csv.append(data["retweeted_status"]["place"]["bounding_box"]["coordinates"])
        else:
            write_to_csv.append(" ")
    elif "quoted_status" in data:
        if "place" in data["quoted_status"] and data["quoted_status"]["place"] is not None and \
                        data["quoted_status"]["place"]["bounding_box"] is not None and \
                        data["quoted_status"]["place"]["bounding_box"]["coordinates"] is not None:
            write_to_csv.append(data["quoted_status"]["place"]["bounding_box"]["coordinates"])
        else:
            write_to_csv.append(" ")
    else:
        write_to_csv.append(" ")
        print "E Coordinates can't found in: ", input_data

    # N place_county_code
    if "place" in data and data["place"] is not None and data["place"]["country_code"] is not None:
        write_to_csv.append(data["place"]["country_code"])
    else:
        write_to_csv.append(" ")

    # O place_county
    if "place" in data:
        if data["place"] is not None:
            if data["place"]["country"] is not None:
                write_to_csv.append(data["place"]["country"].encode('utf-8'))
            else:
                write_to_csv.append(" ")
        else:
            write_to_csv.append(" ")
    else:
        write_to_csv.append(" ")

    # P place_full_name
    if "place" in data and data["place"] is not None and data["place"]["full_name"] is not None:
        write_to_csv.append(data["place"]["full_name"].encode('utf-8'))
    else:
        write_to_csv.append(" ")

    # Q place_name
    if "place" in data and data["place"] is not None and data["place"]["name"] is not None:
        write_to_csv.append(data["place"]["name"].encode('utf-8'))
    else:
        write_to_csv.append(" ")

    # R hashtags
    if "extended_tweet" not in data and "retweeted_status" not in data and "quoted_status" not in data:# tweet only
        if "entities" in data and data["entities"] is not None and data["entities"]["hashtags"] is not None:
            write_to_csv.append(data["entities"]["hashtags"])
        else:
            write_to_csv.append(" ")
    elif "extended_tweet" in data and "retweeted_status" not in data and "quoted_status" not in data:# extended_tweet only
        if "entities" in data["extended_tweet"] and "hashtags" in data["extended_tweet"]["entities"]:
            write_to_csv.append(data["extended_tweet"]["entities"]["hashtags"])
        else:
            write_to_csv.append(" ")
    elif "retweeted_status" in data and "quoted_status" not in data: #retweet only
        if "extended_tweet" not in data["retweeted_status"]:
            if "entities" in data["retweeted_status"] and data["retweeted_status"]["entities"]["hashtags"] is not None:
                write_to_csv.append(data["retweeted_status"]["entities"]["hashtags"])
            else:
                write_to_csv.append(" ")
        elif "extended_tweet" in data["retweeted_status"]:
            if "entities" in data["retweeted_status"]["extended_tweet"] \
                    and "hashtags" in  data["retweeted_status"]["extended_tweet"]["entities"]:
                write_to_csv.append(data["retweeted_status"]["extended_tweet"]["entities"]["hashtags"])
            else:
                write_to_csv.append(" ")
    elif "quoted_status" in data:
        if "extended_tweet" not in data["quoted_status"]:
            if "entities" in data["quoted_status"] and data["quoted_status"]["entities"]["hashtags"] is not None:
                write_to_csv.append(data["quoted_status"]["entities"]["hashtags"])
            else:
                write_to_csv.append(" ")
        elif "extended_tweet" in data["quoted_status"]:
            if "entities" in data["quoted_status"]["extended_tweet"] \
                    and "hashtags" in data["quoted_status"]["extended_tweet"]["entities"]:
                write_to_csv.append(data["quoted_status"]["extended_tweet"]["entities"]["hashtags"])
            else:
                write_to_csv.append(" ")
    else:
        write_to_csv.append(" ")
        print "E hashtags can't found in: ", input_data

    # S media_url_https
    write_to_csv.append([url for url in urls])

    # T extended_url_type
    write_to_csv.append([video_type for video_type in video_types])

    # U type
    write_to_csv.append([type for type in types])

    # V lang
    # useless as it is not original author's
    if "lang" in data and data["lang"] is not None:
        write_to_csv.append(data["lang"])
    else:
        write_to_csv.append(" ")

    # W retweeted_status_tweet_id ---- the original tweet id, can be the id_str from retweeted_status or quoted_status
    # just keep consistence and called it "retweeted_status_tweet_id",
    # in fact, it is also include quoted_status_tweet_id
    if "extended_tweet" not in data and "retweeted_status" not in data and "quoted_status" not in data:# tweet only
        write_to_csv.append(" ")
        id_str = data["id_str"]
    elif "extended_tweet" in data and "retweeted_status" not in data and "quoted_status" not in data:# extended_tweet only
        write_to_csv.append(" ")
        id_str = data["id_str"]
    elif "retweeted_status" in data and "quoted_status" not in data: #retweet only
        if "id_str" in data["retweeted_status"] and data["retweeted_status"]["id_str"] is not None:
            write_to_csv.append(data["retweeted_status"]["id_str"])
            id_str = data["retweeted_status"]["id_str"]
        else:
            write_to_csv.append(" ")
    elif "quoted_status" in data:
        if "id_str" in data["quoted_status"] and data["quoted_status"]["id_str"] is not None:
            write_to_csv.append(data["quoted_status"]["id_str"])
            id_str = data["quoted_status"]["id_str"]
        else:
            write_to_csv.append(" ")
    else:
        write_to_csv.append(" ")
        print "E original id_str can't found in: ", input_data

    # X retweeted_status_user_screen_name
    if "extended_tweet" not in data and "retweeted_status" not in data and "quoted_status" not in data:# tweet only
        write_to_csv.append(" ")
        screen_name = data["user"]["screen_name"]
    elif "extended_tweet" in data and "retweeted_status" not in data and "quoted_status" not in data:# extended_tweet only
        write_to_csv.append(" ")
        screen_name = data["user"]["screen_name"]
    elif "retweeted_status" in data and "quoted_status" not in data: #retweet only
        if "user" in data["retweeted_status"] and data["retweeted_status"]["user"] is not None and \
                        data["retweeted_status"]["user"]["screen_name"] is not None:
            write_to_csv.append(data["retweeted_status"]["user"]["screen_name"])
            screen_name = data["retweeted_status"]["user"]["screen_name"]
        else:
            write_to_csv.append(" ")
    elif "quoted_status" in data:
        if "user" in data["quoted_status"] and data["quoted_status"]["user"] is not None and \
                        data["quoted_status"]["user"]["screen_name"] is not None:
            write_to_csv.append(data["quoted_status"]["user"]["screen_name"])
            screen_name = data["quoted_status"]["user"]["screen_name"]
        else:
            write_to_csv.append(" ")
    else:
        write_to_csv.append(" ")
        print "E original user_screenname can't found in: ", input_data

    # Y tweet_link ---- original tweet link, it can be the original tweet in retweet or quoted tweet
    write_to_csv.append("https://twitter.com/" + str(screen_name) + "/status/" + str(id_str))
    writer.writerow(write_to_csv)

for filename in original_download_file_list:
    filename = os.path.splitext(filename)[0]
    print filename
    source_json_path = source_dir + filename + '.json'
    result_file_path = result_dir + filename + '.csv'
    with open(result_dir + "invalid_" +filename +".json", "w") as invalid_json_f:
        writer_invalid = csv.writer(invalid_json_f)

        with open(result_file_path, "w") as f:
            writer = csv.writer(f)

            writer.writerow(
                ["source_file", "created_at", "retweeted_status_created_at", "tweet_id", "tweet_text", "user_id", "user_name", "user_screen_name", "user_location",
                 "user_time_zone", "user_lang", "coordinates", "place_bounding_box", "place_country_code", "place_country", "place_full_name",
                 "place_name", "hashtags", "media_url_https", "extended_url_type", "type", "lang", "retweeted_status_tweet_id",
                 "retweeted_status_user_screen_name", "tweet_link"])

            # for file in files:
            # filename = "hurricane_twitter.json" # os.path.basename(file)

            with io.open(source_json_path, encoding="utf-8") as data_file:
                for line in data_file:
                    try:
                        if line != "\n" and not line.startswith('{"limit"'):
                            total_json += 1
                            # print (line)
                            data = json.loads(line)
                            generate_csv(data)
                            parsed_csv += 1
                            print parsed_csv
                    except Exception as e:
                        print(e)
                        print (line)
                        try:

                            demjson.decode(line)
                            generate_csv(data)
                            parsed_csv_smart += 1
                        except Exception as e:
                            print(e)

                            print (line)
                            writer_invalid.writerow(line)
                            invalid_json += 1
                            continue
                print (
                "total_json", total_json, "parsed_csv", parsed_csv, "parsed_csv_smartjson", parsed_csv_smart, "invalid_json",
                invalid_json)



