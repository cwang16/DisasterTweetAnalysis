import pandas
import os, io
import re
import csv
import gc
from collections import defaultdict


# read socical media dataset
field_name = "hashtags"
#field_name = "tweet_cleaned"  # hashtags   or tweet_text or tweet_cleaned
source_dir = "/media/"
result_dir = "/media/"
keywordfile_path = "/media/keyword.txt"
result_dir_hashtags_tweet_cleaned = result_dir + field_name
if not os.path.exists(result_dir_hashtags_tweet_cleaned):
    os.makedirs(result_dir_hashtags_tweet_cleaned)
statistic_file_path = os.path.join(result_dir_hashtags_tweet_cleaned, "statistics" + ".csv")

original_coordinate_box_both = "both"
dir_list = os.listdir(source_dir)
csv_file_list = []
keyword_list = []
no_space_keyword_list = []
total_keyword_list = []
counter = 0
result_dict = {}
result_dict = defaultdict(lambda : 0, result_dict)

def pywalker(path, name):
    global counter, csv_file_list
    for root, dirs, files in os.walk(path):
        for file_ in files:
            whole_file_name = name + ".csv"
            if file_.__contains__(whole_file_name):
                locals()
                csv_file_list.append(os.path.join(root, file_))
                counter += 1
    return counter


def read_keyword(path_keyword):
    with io.open(path_keyword, encoding="utf-8") as keyword_file:
        for line in keyword_file:
            keyword_list.append(line.encode("utf-8").rstrip('\n'))
    return len(keyword_list)


def add_nospace_keyword (word_list):
    for word in word_list:
        if " " in word:
            no_space_word = word.replace(" ", "")
            no_space_keyword_list.append(no_space_word)
    return len(no_space_keyword_list)

def write_to_csv(fm_to_write, reslut_dir, base_filename, keyWord):

    csv_path = os.path.join(reslut_dir, base_filename + "_______" + keyWord + ".csv")
    fm_to_write.to_csv(csv_path, mode='a', header=False, index=False, encoding = 'utf-8')

def initiate():
    print "total files: ", pywalker(source_dir, original_coordinate_box_both)
    print "keyword with space: ", read_keyword(keywordfile_path)
    print "keyword without space: ", add_nospace_keyword(keyword_list)
    total_keyword_list = keyword_list + no_space_keyword_list
    print "------------keyword_list including no space-------------------\n", total_keyword_list

def write_dict_to_csv(result_p, result):
    with open(result_p, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in result.items():
            writer.writerow([key, value])


def release_df(df):
    del [df]
    gc.collect()
    df = pandas.DataFrame()


initiate()
for keyword in keyword_list:
    print "---------------", keyword, "-------------------"
    for file_path in csv_file_list:
        count_row = 0
        count_row_no_space = 0
        split_list = file_path.split("/")  # split string into a list
        base_filename = split_list[len(split_list)-2]
        df_twitter = pandas.read_csv(file_path, lineterminator='\n', encoding="utf-8", header=0, error_bad_lines = False, index_col = False, dtype = 'unicode')
        df_twitter = df_twitter.fillna('missing')
        new_frame = pandas.DataFrame
        new_frame_no_space = pandas.DataFrame
        new_frame = df_twitter[df_twitter[field_name].str.contains(keyword, case=False)] #case insentitive
        count_row = new_frame.shape[0]  # gives number of row count
        result_dict[keyword] += count_row
        print count_row, "found in", split_list[-1]

        if " " in keyword:
            no_space_word = keyword.replace(" ", "")
            new_frame_no_space = df_twitter[df_twitter[field_name].str.contains(no_space_word, case=False)]  # case insentitive
            count_row_no_space = new_frame_no_space.shape[0]  # gives number of row count
            result_dict[keyword] += count_row_no_space
            print count_row_no_space, "(no space keyword) found in", split_list[-1]

        if count_row > 1:
            if count_row_no_space > 1:
                new_frame = new_frame.append(new_frame_no_space)
            write_to_csv(new_frame, result_dir_hashtags_tweet_cleaned, base_filename, keyword)
        release_df(new_frame)
        release_df(new_frame_no_space)

write_dict_to_csv(statistic_file_path, result_dict)
















