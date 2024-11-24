import csv
import os
import sqlite3
import urllib.request

# import urllib.request

CREATE_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS procurement (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL UNIQUE,
    product_price INTEGER NOT NULL,
    product_customers_count INTEGER NOT NULL,
    product_links TEXT NOT NULL,
    product_image_links TEXT NOT NULL
);
"""

CREATE_IMAGE_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_link TEXT NOT NULL UNIQUE,
    image_filepath TEXT NOT NULL UNIQUE,
    product_id INT NOT NULL UNIQUE,
    FOREIGN KEY (product_id)
    REFERENCES procurement (product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

INSERT_DATA_INTO_TABLE = """
INSERT INTO procurement (product_name, product_price, product_customers_count, product_links, product_image_links)
VALUES(?, ?, ?, ?, ?)
"""

INSERT_DATA_INTO_IMAGE_TABLE = """
INSERT INTO images (image_link, image_filepath, product_id)
VALUES(?, ?, ?)
"""

DELETE_DATA_FROM_TABLE = """
DELETE FROM procurement where product_image_link = ?
"""


def is_created(folder="databases"):
    try:
        os.mkdir(folder)
        return False
    except FileExistsError:
        return True


def create_tables(statement=CREATE_TABLE_STATEMENT):
    if is_created():
        with sqlite3.connect("databases/procurement.db") as procurement_db:
            cursor = procurement_db.cursor()
            cursor.execute(statement)
            procurement_db.commit()
            cursor.close()
    else:
        pass


def retrieve_csv_files(folder, filename):
    with open(os.path.join(os.getcwd(), "{}/{}.csv".format(folder, filename))) as csv_file:
        reader = csv.reader(csv_file)
        contents = list(reader)[1:]

    new_contents = []

    for content in contents:
        normalized_contents = []
        for element in content:
            if element.isdigit():
                normalized_contents.append(int(element))
            else:
                normalized_contents.append(element)
        new_contents.append(tuple(normalized_contents))

    return new_contents


def insert_data(statement, entries=None):
    if entries is not None:
        with sqlite3.connect("databases/procurement.db") as procurement_db:
            cursor = procurement_db.cursor()
            for entry in entries:
                try:
                    cursor.execute(statement, entry)
                except sqlite3.IntegrityError:
                    pass
            procurement_db.commit()
            cursor.close()
    else:
        pass


def insert_data_from_folder(folder="resources"):
    for file in os.listdir(os.path.join(os.getcwd(), folder)):
        insert_data(INSERT_DATA_INTO_TABLE, retrieve_csv_files("resources", file.removesuffix(".csv")))


def select_data_from_database(table_name):
    with sqlite3.connect("databases/procurement.db") as procurement_db:
        cursor = procurement_db.cursor()
        cursor.execute('SELECT * FROM {}'.format(table_name))
        rows = cursor.fetchall()

    return rows


def select_data_from_database_by_id(_id: int):
    with sqlite3.connect("databases/procurement.db") as procurement_db:
        cursor = procurement_db.cursor()
        cursor.execute('SELECT * FROM procurement where product_id = ?', (_id, ))
        selected_row = cursor.fetchone()

    return selected_row


def select_data_from_database_by_rows(rows: int):
    with sqlite3.connect("databases/procurement.db") as procurement_db:
        cursor = procurement_db.cursor()
        cursor.execute('SELECT * FROM procurement')
        selected_rows = cursor.fetchmany(rows)

    return selected_rows


# if __name__ == "__main__":
#     create_tables()
#     insert_data_from_folder()

def get_product_identity_for_deleting_data():
    product_id = []
    for index, row in enumerate(select_data_from_database("procurement")):
        if str(row[-1]).startswith("https://assets.tokopedia.net/") or str(row[-1]) == "Tautan Citra":
            product_id.append(row[0])

    return product_id


def deleting_data_from_table_by_specific_product_identity(_id_list: list):
    with sqlite3.connect("databases/procurement.db") as procurement_db:
        cursor = procurement_db.cursor()
        for _id_ in _id_list:
            cursor.execute('DELETE FROM procurement WHERE product_id = ?', (_id_, ))
        procurement_db.commit()
        cursor.close()


def get_image_id_for_deleting_data():
    image_id = []
    for row in select_data_from_database("images"):
        if str(row[1]).startswith("images") or str(row[2]).startswith("https://images.tokopedia.net/"):
            image_id.append(row[0])

    return image_id


def deleting_data_from_table_by_specific_image_identity(_id_list: list):
    with sqlite3.connect("databases/procurement.db") as procurement_db:
        cursor = procurement_db.cursor()
        for _id_ in _id_list:
            cursor.execute('DELETE FROM images WHERE image_id = ?', (_id_,))
        procurement_db.commit()
        cursor.close()


if __name__ == "__main__":
    insert_data_from_folder("resources")
    deleting_data_from_table_by_specific_product_identity(get_product_identity_for_deleting_data())
    images_content = []
    for data_index, data_row in enumerate(select_data_from_database("procurement")):
        image_path = "images\\image_{}.png".format(str(data_row[0]).zfill(3))
        image_link = str(data_row[-1]).removesuffix("?ect=4g")
        product_identity = data_row[0]
        images_content.append((image_link, image_path, product_identity))

    insert_data(INSERT_DATA_INTO_IMAGE_TABLE, images_content)
    deleting_data_from_table_by_specific_image_identity(get_image_id_for_deleting_data())

    for row in select_data_from_database("images"):
        urllib.request.urlretrieve(row[1].replace(".png", "").replace(".jpeg", ""), row[2])
