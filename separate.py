#step1:change base_Filename = "your file just download from cislinux"

import pandas
import os, io
import re
import sys;
reload(sys);
sys.setdefaultencoding("utf8")


src_dir ="/media/"
out_dir ="/media/"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

csv_file_list = os.listdir(src_dir)

final_total = 0
final_box = 0
final_both = 0
final_coordinate = 0

def generate_filtered_files(full_path, base_filename, output_dir):
    df_twitter = pandas.read_csv(full_path,lineterminator='\n', encoding = "utf-8", header=0)

    contains_coordinate = pandas.DataFrame()  # creates a new dataframe that's empty
    contains_box = pandas.DataFrame()  # creates a new dataframe that's empty
    contains_box = pandas.DataFrame()  # creates a new dataframe that's empty
    contains_both = pandas.DataFrame()  # creates a new dataframe that's empty

    contains_coordinate = df_twitter[df_twitter['coordinates'].str.match('\[')]
    contains_box = df_twitter[df_twitter['place_bounding_box'].str.match('\[\[\[')]
    contains_both = contains_coordinate[contains_coordinate['place_bounding_box'].str.match('\[\[\[')]

    count_total = df_twitter.shape[0]  # gives number of row count
    count_coordinate = contains_coordinate.shape[0]  # gives number of row count
    count_box = contains_box.shape[0]  # gives number of row count
    count_both = contains_both.shape[0]  # gives number of row count

    filename_suffix = "csv"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    new_folder_path = os.path.join(output_dir, base_filename)


    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        original_csv_path = os.path.join(new_folder_path, "original" + "." + filename_suffix)
        coordinate_csv_path = os.path.join(new_folder_path, "coordinate" + "." + filename_suffix)
        box_csv_path = os.path.join(new_folder_path, "box" + "." + filename_suffix)
        both_csv_path = os.path.join(new_folder_path, "both" + "." + filename_suffix)
        df_twitter.to_csv(original_csv_path)
        contains_box.to_csv(box_csv_path)
        contains_coordinate.to_csv(coordinate_csv_path)
        contains_both.to_csv(both_csv_path)

    filename_suffix = "txt"
    txt_path = os.path.join(output_dir, base_filename + "." + filename_suffix)
    with open(txt_path, "a") as file:
        write_to_txt = "-------" + base_filename + "-------" + "\ntotal: " + str(
            count_total) + "\n" + "coordinate: " + str(count_coordinate) + "\n" + "box: " + str(
            count_box) + "\n" + "both: " + str(count_both)
        file.write(write_to_txt)

    global final_total
    final_total += count_total
    global final_box
    final_box += count_box
    global final_coordinate
    final_coordinate += count_coordinate
    global final_both
    final_both += count_both

    print "________________________", filename, "_____________________________"
    print "total: ", count_total
    print "coordinate: ", count_coordinate
    print "box: ", count_box
    print "both: ", count_both

for filename in csv_file_list:
    if filename.endswith(".csv"):
        no_extension = os.path.splitext(filename)[0]
        srcPath = src_dir + filename
        generate_filtered_files(srcPath, no_extension, out_dir)
print ("________________________Summary_____________________________")
print "final total: ", final_total
print "final_coordinate: ", final_coordinate
print "final_box: ", final_box
print "final_both: ", final_both























