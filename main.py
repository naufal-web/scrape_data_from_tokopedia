from functions.scrape_data_from_tokopedia import ScrapeDataFromTokopedia
import csv

contents = []
extensive_contents = []

scraper = ScrapeDataFromTokopedia("brankas", 2, 18)
scraper.search()

for element in scraper.temporary_elements:
    rows = []
    for ele in element:
        if ele.startswith("Rp"):
            price = int(ele.removeprefix("Rp").replace(".", ""))
            print(price, end=" ")
            rows.append(price)
        elif ele.endswith(" terjual"):
            historical_selling = ele.removesuffix(" terjual")
            if historical_selling.endswith("rb+"):
                historical_selling = int(historical_selling.removesuffix("rb+")) * 1000
                print(historical_selling, end=" ")
                rows.append(historical_selling)
            elif historical_selling.endswith("jt+"):
                historical_selling = int(historical_selling.removesuffix("jt+")) * 1000000
                print(historical_selling, end=" ")
                rows.append(historical_selling)
            elif historical_selling.endswith("+"):
                historical_selling = int(historical_selling.removesuffix("+"))
                print(historical_selling, end=" ")
                rows.append(historical_selling)
            else:
                historical_selling = int(historical_selling)
                print(historical_selling, end=" ")
                rows.append(historical_selling)
        else:
            print(ele, end=" ")
            rows.append(ele)
    print()
    contents.append(rows)


try:
    with open(f"resources/{scraper.query.replace("+", "_")}.csv", mode="x", newline="", encoding="UTF-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Nama Produk", "Harga Produk", "Jumlah Barang Produk Yang Terjual"])
        csv_writer.writerows(contents)
except FileExistsError:
    # no_duplicate_contents = list(set(contents))

    sett = set()

    for content in contents:
        sett.add(tuple(content))

    for content in contents:
        content = tuple(content)
        if content not in sett:
            extensive_contents.append(list(content))

    with open(f"resources/{scraper.query.replace("+", "_")}.csv", mode="a", newline="", encoding="UTF-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(extensive_contents)