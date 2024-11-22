# from functions.scrape_data_from_tokopedia import ScrapeDataFromTokopedia
import csv
import string
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

indonesian_stopwords = stopwords.words("indonesian")
english_stopwords = stopwords.words("english")

bilingual_stopwords = indonesian_stopwords + english_stopwords

indonesian_stemmer_factory = StemmerFactory()
indonesian_stemmer = indonesian_stemmer_factory.create_stemmer(True)

indonesian_local_stopwords = StopWordRemoverFactory().create_stop_word_remover()

with open(r"C:\Users\62853\PycharmProjects\cashier_app\resources\brankas_terbaik.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    for content in list(csv_reader)[1:]:
        name, price, historical_selling = content
        no_punctuation_name = name.translate(str.maketrans('', '', string.punctuation))
        no_digit_name = no_punctuation_name.translate(str.maketrans('', '', string.digits))
        lower_case_name = no_digit_name.replace('   ', ' ').replace('  ', ' ').lower()
        tokenized_name = lower_case_name.split(" ")
        no_stopwords_name = [token for token in tokenized_name if token not in bilingual_stopwords]
        indonesian_stemmed_name = [indonesian_stemmer.stem(word) for word in no_stopwords_name]
        print(" ".join(indonesian_stemmed_name))

# contents = []
# extensive_contents = []
#
# scraper = ScrapeDataFromTokopedia("brankas terlaris", 0, 18)
# scraper.search()
#
# for element in scraper.temporary_elements:
#     rows = []
#     for ele in element:
#         if ele.startswith("Rp"):
#             price = int(ele.removeprefix("Rp").replace(".", ""))
#             print(price, end=" ")
#             rows.append(price)
#         elif ele.endswith(" terjual"):
#             historical_selling = ele.removesuffix(" terjual")
#             if historical_selling.endswith("rb+"):
#                 historical_selling = int(historical_selling.removesuffix("rb+")) * 1000
#                 print(historical_selling, end=" ")
#                 rows.append(historical_selling)
#             elif historical_selling.endswith("jt+"):
#                 historical_selling = int(historical_selling.removesuffix("jt+")) * 1000000
#                 print(historical_selling, end=" ")
#                 rows.append(historical_selling)
#             elif historical_selling.endswith("+"):
#                 historical_selling = int(historical_selling.removesuffix("+"))
#                 print(historical_selling, end=" ")
#                 rows.append(historical_selling)
#             else:
#                 historical_selling = int(historical_selling)
#                 print(historical_selling, end=" ")
#                 rows.append(historical_selling)
#         else:
#             print(ele, end=" ")
#             rows.append(ele)
#     print()
#     contents.append(rows)
#
#
# try:
#     with open(f"resources/{scraper.query.replace("+", "_")}.csv", mode="x", newline="", encoding="UTF-8") as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(["Nama Produk", "Harga Produk", "Jumlah Barang Produk Yang Terjual"])
#         csv_writer.writerows(contents)
# except FileExistsError:
#
#     with open(f"resources/{scraper.query.replace("+", "_")}.csv", mode="r", newline="", encoding="UTF-8") as csv_file:
#         existed_content = list(csv.reader(csv_file))[1:]
#
#     for content in contents:
#         content = tuple(content)
#         if content not in existed_content:
#             extensive_contents.append(content)
#
#     with open(f"resources/{scraper.query.replace("+", "_")}.csv", mode="a", newline="", encoding="UTF-8") as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerows(extensive_contents)