import time
from urllib3.exceptions import *
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import *
from bs4.__init__ import BeautifulSoup
from datetime import datetime


class ScrapeDataFromTokopedia:

    def __init__(self, query, page_start: int, page_end: int):
        self.scripts = None
        self.query = query
        self.soup = None
        self.current_elements = None
        self.current_element = None
        self.temporary_elements = set()
        # self.temporary_elements = [
        #     ("Nama Produk", "Harga Produk", "Jumlah Barang Yang Terjual", "Tautan Produk", "Tautan Citra")]
        self.temporary_elements.add(
            ("Nama Produk", "Harga Produk", "Jumlah Barang Yang Terjual", "Tautan Produk", "Tautan Citra"))
        self.maximum_pages = 100
        self.page_start = page_start
        self.page_end = page_end
        self.page_range = range(self.page_start, self.page_end)
        self.search()

    def print_result(self):
        self.current_element = self.soup.find("div", id="zeus-root")
        self.soup = self.current_element

        classes = ["css-8atqhb", "css-jau1bt", "css-rjanld"]

        for class_ in classes:
            self.current_element = self.soup.find("div", class_=class_)
            self.soup = self.current_element

        self.current_element = self.soup.find(attrs={"data-testid": "divSRPContentProducts"})
        self.soup = self.current_element

        try:
            self.current_elements = self.soup.find_all("div", class_="css-jza1fo")
            self.soup = self.current_elements
        except AttributeError:
            pass
        else:
            pass

        if self.soup is not None:
            for element in self.soup:
                sub_elements = element.find_all("div", class_="css-5wh65g")
                # print(sub_elements)
                for child_element in sub_elements:
                    child_element = child_element.find("a", class_="oQ94Awb6LlTiGByQZo8Lyw== IM26HEnTb-krJayD-R0OHw==")
                    # print(child_element)
                    if child_element is not None:
                        class_name_for_normal_price = "_67d6E1xDKIzw+i2D2L0tjw== "
                        class_name_for_current_price = "_67d6E1xDKIzw+i2D2L0tjw== t4jWW3NandT5hvCFAiotYg=="
                        # class_name_for_previous_price = "q6wH9+Ht7LxnxrEgD22BCQ=="
                        product_link = child_element.get("href")
                        child_element = child_element.find("div", class_="bYD8FcVCFyOBiVyITwDj1Q==")
                        product_image_link = child_element.find("img")
                        product_image_link = product_image_link.get("src")
                        product_name = child_element.find("span", class_="_0T8-iGxMpV6NEsYEhwkqEg==")
                        normal_price = child_element.find("div", class_=class_name_for_normal_price)
                        current_price = child_element.find("div", class_=class_name_for_current_price)
                        sold_number = child_element.find("span", class_="se8WAnkjbVXZNA8mT+Veuw==")
                        # previous_price = child_element.find("span", class_=class_name_for_previous_price)
                        if normal_price is not None and current_price is None and sold_number is not None:
                            normal_price = normal_price.text.replace("Rp", "").replace(".", "")
                            if sold_number.text.find("+ terjual") > 0:
                                sold_number = sold_number.text.replace("+ terjual", "")
                            else:
                                sold_number = sold_number.text.replace(" terjual", "")
                            self.temporary_elements.add((product_name.text, normal_price, sold_number, product_link,
                                                         product_image_link))
                        elif current_price is not None and normal_price is None and sold_number is not None:
                            current_price = current_price.text.replace("Rp", "").replace(".", "")
                            if sold_number.text.find("+ terjual") > 0:
                                sold_number = sold_number.text.replace("+ terjual", "")
                            else:
                                sold_number = sold_number.text.replace(" terjual", "")
                            self.temporary_elements.add((product_name.text, current_price, sold_number, product_link,
                                                        product_image_link))
        else:
            pass

        # self.temporary_elements = list(set(self.temporary_elements))

    def search(self):
        self.query = self.query.replace(" ", "+")
        for m in self.page_range:
            driver = WebDriver()
            try:
                driver.get("https://www.tokopedia.com/search?navsource=&page={}&q={}".format(m + 1, self.query))
            except NoSuchWindowException:
                continue
            except ReadTimeoutError:
                break

            self.scripts = []
            try:
                for k in range(110):
                    driver.execute_script("window.scrollBy({}, {});".format(k, k + 1))
                    time.sleep(0.05)
                    if k % 30 == 0:
                        self.scripts.append(driver.page_source)
                if datetime.now().second < 60:
                    time.sleep(60.0 - float(datetime.now().second))
                    self.scripts.append(driver.page_source)
                else:
                    time.sleep(0.0)
                    self.scripts.append(driver.page_source)
            except NoSuchWindowException:
                driver.close()
                continue
            except ReadTimeoutError:
                driver.close()
                continue
            except InvalidSessionIdException:
                driver.close()
                continue
            except WebDriverException:
                driver.close()
                continue
            else:
                driver.close()
                for script in self.scripts:
                    self.soup = BeautifulSoup(script, "html.parser")
                    self.print_result()
                    continue

            print("Halaman {}/{}".format(str(m + 1).zfill(3), str(self.page_end).zfill(3)))
            print("Data yang diterima secara kumulatif : {} data".format(len(list(self.temporary_elements)[1:])))
