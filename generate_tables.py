import csv

# this code is specifically for the customers .csv file and table, so it has to be modified for the other tables
# by change I mean change the colums which contain the data we need


# commenting these out and putting default names
# file_name = input("Input the source file name. Remember to put '.csv' at the end. \n")
# dest_name = input("Input the destination file name. This is where the output will be stored. Remember to put '.csv' at the end. \n")

# CHANGE THESE FOR THE OTHER FILES
file_name = "olist_customers_dataset.csv"
dest_name = "customers_table.csv"

with open(file_name, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader)                # this skips the lines with the headers
    line1_flag = True               # to check if we are looking at the first line

    with open(dest_name, 'w', newline="") as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(["customer_id", "customer_postal_code"]) # CHANGE THESE FOR THE OTHER FILES
        
        for line in csv_reader:
            # this will iterate over every record and put the customer_id and customer_postal_code
            # in the destination file
            # remember I've skipped the line with headings
            # line[0] is customer_id and line[2] is customer_zip_code_prefix
            # CHANGE THESE FOR THE OTHER FILES
            
            csv_writer.writerow([line[0],line[2]])