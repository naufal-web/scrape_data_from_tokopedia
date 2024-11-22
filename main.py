from functions.scrape_data_from_tokopedia import ScrapeDataFromTokopedia
import csv

contents = []
extensive_contents = []

scraper = ScrapeDataFromTokopedia("brankas terbaru", 2, 18)
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

    with open(f"resources/{scraper.query.replace("+", "_")}.csv", mode="r", newline="", encoding="UTF-8") as csv_file:
        existed_content = list(csv.reader(csv_file))[1:]

    for content in contents:
        content = tuple(content)
        if content not in existed_content:
            extensive_contents.append(content)

    with open(f"resources/{scraper.query.replace("+", "_")}.csv", mode="a", newline="", encoding="UTF-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(extensive_contents)