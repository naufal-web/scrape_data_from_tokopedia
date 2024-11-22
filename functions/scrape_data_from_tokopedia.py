import time

import urllib3.exceptions
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import *
from bs4.__init__ import BeautifulSoup


class ScrapeDataFromTokopedia:

    def __init__(self, query, page_start: int, page_end: int):
        self.scripts = None
        self.query = query
        self.soup = None
        self.current_elements = None
        self.current_element = None
        self.temporary_elements = []
        self.maximum_pages = 100
        self.page_start = page_start
        self.page_end = page_end
        self.page_range = range(self.page_start, self.page_end)

    def print_result(self):
        self.current_element = self.soup.find("div", id="zeus-root")
        self.soup = self.current_element

        self.current_element = self.soup.find("div", class_="css-8atqhb")
        self.soup = self.current_element

        self.current_element = self.soup.find("div", class_="css-jau1bt")
        self.soup = self.current_element

        self.current_element = self.soup.find("div", class_="css-rjanld")
        self.soup = self.current_element

        self.current_element = self.soup.find(attrs={"data-testid": "divSRPContentProducts"})
        self.soup = self.current_element

        try:
            self.current_elements = self.soup.find_all("div", class_="css-jza1fo")
            self.soup = self.current_elements
        except AttributeError:
            self.current_element = self.soup.find("div", class_="IOLazyLoading")
            self.current_elements = self.current_element.find_all("div", class_="css-jza1fo")
            self.soup.extend(self.current_elements)
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
                        child_element = child_element.find("div", class_="bYD8FcVCFyOBiVyITwDj1Q==")
                        product_name = child_element.find("span", class_="_0T8-iGxMpV6NEsYEhwkqEg==")
                        normal_price = child_element.find("div", class_=class_name_for_normal_price)
                        current_price = child_element.find("div", class_=class_name_for_current_price)
                        sold_number = child_element.find("span", class_="se8WAnkjbVXZNA8mT+Veuw==")
                        # previous_price = child_element.find("span", class_=class_name_for_previous_price)
                        if normal_price is not None and current_price is None and sold_number is not None:
                            self.temporary_elements.append([product_name.text, normal_price.text, sold_number.text])
                            # print(product_name.text, normal_price.text)
                        elif current_price is not None and normal_price is None and sold_number is not None:
                            self.temporary_elements.append([product_name.text, current_price.text, sold_number.text])
                            # print(product_name.text, current_price.text)
        else:
            self.temporary_elements.append([])

    def search(self):
        self.query = self.query.replace(" ", "+")
        for m in self.page_range:
            try:
                driver = WebDriver()
                driver.get("https://www.tokopedia.com/search?navsource=&page={}&q={}".format(m+1, self.query))
                for k in range(0, 3000, 600):
                    driver.execute_script(" window.scrollBy({}, {});".format(k, k+600))
                    time.sleep(12.)
                self.scripts = driver.page_source
                driver.close()
            except NoSuchWindowException:
                pass
            except urllib3.exceptions.ReadTimeoutError:
                pass
            else:
                self.soup = BeautifulSoup(self.scripts, "html.parser")
                self.print_result()
