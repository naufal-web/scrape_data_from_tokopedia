import csv
import os.path
from urllib.request import urlretrieve

resource_dir = os.path.join(os.getcwd(), "resources")

resource_names = [file.replace(".csv", "")
                  for file in os.listdir(resource_dir)
                  if file.find("_") > 0]

resource_files = [os.path.join(resource_dir, file)
                  for file in os.listdir(resource_dir)
                  if file.find("_") > 0]

for resource_name, resource_file in zip(resource_names, resource_files):
    with open(resource_file, mode="r", newline="", encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file)

        try:
            os.mkdir(os.path.join(os.getcwd(), "images"))
        except FileExistsError:
            pass

        for index, content in enumerate(list(csv_reader)[1:]):
            stored_path = os.path.join(os.getcwd(), "images\\{}_{}.png".format(resource_name, str(index+1).zfill(2)))
            urlretrieve(content[-1].replace(".webp?ect=4g", ""), stored_path)