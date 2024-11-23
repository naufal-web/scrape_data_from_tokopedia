import os
import csv
from functions.scrape_data_from_tokopedia import ScrapeDataFromTokopedia

root_path = os.getcwd()
resources_dir = "resources"
filename = "brankas"
filenames = [filename + name for name in ["_terbaik", "_terbaru", "_terlaris", "_termurah"]]

csv_extensions = ".csv"

for file_state in filenames:
    query = file_state.replace("_", "+")

    saving_filepath = os.path.join(root_path, resources_dir, file_state + csv_extensions)

    print(saving_filepath)

    tokopedia = ScrapeDataFromTokopedia(query, 0, 28)
    for content in tokopedia.temporary_elements:
        print(content)

    with open(saving_filepath, mode="w", newline="", encoding="UTF-8") as saved_filepath:
        file_writer = csv.writer(saved_filepath)
        file_writer.writerows(tokopedia.temporary_elements)