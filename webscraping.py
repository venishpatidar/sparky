from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get("https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&honors=F&promod=F&searchType=all&term=2251")

time.sleep(5)

page_html = driver.page_source

with open("asu_class_schedule.html", "w", encoding='utf-8') as file:
    file.write(page_html)
driver.quit()
