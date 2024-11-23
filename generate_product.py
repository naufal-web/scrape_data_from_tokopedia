import os
import csv
from functions.scrape_data_from_tokopedia import ScrapeDataFromTokopedia

root_path = os.getcwd()
resources_dir = "resources"
filename = "brankas_terlaris"
csv_extensions = ".csv"
query = filename.replace("_", "+")

saving_filepath = os.path.join(root_path, resources_dir, filename + csv_extensions)

tokopedia = ScrapeDataFromTokopedia(query, 0, 19)
for content in tokopedia.temporary_elements:
    print(content)

with open(saving_filepath, mode="w", newline="", encoding="UTF-8") as saved_filepath:
    file_writer = csv.writer(saved_filepath)
    file_writer.writerows(tokopedia.temporary_elements)