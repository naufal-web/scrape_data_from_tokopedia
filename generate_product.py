import os
import csv
from functions.scrape_data_from_tokopedia import ScrapeDataFromTokopedia
from urllib.request import urlretrieve


class UpdateResources(ScrapeDataFromTokopedia):

    root_path = os.getcwd()
    resources_dir = "resources"
    filename = "brankas"
    csv_extensions = ".csv"

    def retrieve_csv_file(self):
        with open(self.savable_filepath, mode="r", newline="", encoding="UTF-8") as existing_filepath:
            reader = csv.reader(existing_filepath)
            existing_content = list(reader)[1:]

        return existing_content

    def get_new_data(self):
        new_contents = []
        for new_or_existed_content in self.temporary_elements:
            if new_or_existed_content not in self.existing_content:
                new_contents.append(new_or_existed_content)

        return new_contents

    def append_to_existing_data(self):
        with open(self.savable_filepath, mode="a", newline="", encoding="UTF-8") as existing_filepath:
            writer = csv.writer(existing_filepath)
            writer.writerows(self.filtrated_content)

    def creating_new_data(self):
        with open(self.savable_filepath, mode="x", newline="", encoding="UTF-8") as new_filepath:
            writer = csv.writer(new_filepath)
            writer.writerows(self.temporary_elements)

    def retrieve_new_images(self, file):
        for index, content in enumerate(self.temporary_elements[1:]):
            new_images_path = "images\\{}_{}.png".format(file, str(index + 1).zfill(2))
            stored_path = os.path.join(self.root_path, new_images_path)
            urlretrieve(content[-1].replace(".webp?ect=4g", ""), stored_path)

    def __init__(self, new_or_existed_query: str, start_index, end_index):
        categories = ["_terbaik", "_terbaru", "_terlaris", "_termurah"]
        self.filenames = [new_or_existed_query + name for name in categories]
        if new_or_existed_query == self.filename:
            for file in self.filenames:
                super().__init__(query=file.replace("_", "+"), page_start=start_index, page_end=end_index)
                self.savable_filepath = os.path.join(self.root_path, self.resources_dir, file + self.csv_extensions)
                self.existing_content = self.retrieve_csv_file()
                self.filtrated_content = self.get_new_data()
                self.append_to_existing_data()
                self.retrieve_new_images(file)

        else:
            self.filename = new_or_existed_query
            self.filenames.insert(0, self.filename)
            for file in self.filenames:
                super().__init__(query=file.replace("_", "+"), page_start=0, page_end=end_index)

                self.savable_filepath = os.path.join(self.root_path, self.resources_dir, file + self.csv_extensions)
                self.creating_new_data()
                self.retrieve_new_images(file)


update_resources = UpdateResources(new_or_existed_query="mesin_bubut", start_index=0, end_index=13)