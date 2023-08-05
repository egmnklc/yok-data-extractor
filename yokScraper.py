import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
# taken from https://selenium-python.readthedocs.io/waits.html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# taken from https://stackoverflow.com/questions/33811752/opening-chromedriver-in-fullscreen-selenium-and-python
from selenium.webdriver.chrome.options import Options
import json
from datetime import datetime
start_time = datetime.now()

url = 'https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p=say'

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
# chromeOptions.add_experimental_option("detach", True) # Prevent browser to exit immidiately after script ends. Fixed stale element issue by commenting it out.    

# chromeOptions.add_argument("--kiosk")

# Create a new Chrome session
# Would like chrome to start in fullscreen
driver = webdriver.Chrome(options=chromeOptions)
driver.maximize_window()
# set display options for pandas
# pd.options.display.max_columns = 255
# pd.options.display.max_colwidth = 255

# Load the web page
driver.get(url)
# driver.execute_script("document.body.style.zoom='50%'")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# driver.implicitly_wait(10)
# time.sleep(10)
# click on the "Next" page
# WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
#     (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/ul/li[9]"))).click()

# max number of pagination
MAXVALUE = int(WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/ul/li[8]"))).text)
min_value = 1
print(MAXVALUE)

f = open("yokData_Test.json", "w+", encoding="UTF-8")
f.write('{ "Page_1": ')
# Keep clicking on next until MAXVALUE
for i in range(0, MAXVALUE+1):
    # print("IN LOOP")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tables = soup.find_all('table')
    dfs = pd.read_html(str(tables))
    # print(type(dfs[0]))
    # print(str(dfs[0]))

    result = dfs[0].to_json(orient="index")
    parsed = json.loads(result)
    string = json.dumps(parsed, indent=5, ensure_ascii=False).encode('utf8')
    # print dataframe object in json format with utf-8 encoding
    resultString = string.decode('utf-8')
    f.write(string.decode())
    # print(resultString)
    # declare a button so each time dom updates it can fetch, otherwise gives error.
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/ul/li[9]/a")))
    # button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    #     (By.XPATH, "//button[contains(., 'Sonraki')]")))
    driver.implicitly_wait(1)
    button.click()
    # print("Min value is:", min_value)
    min_value += 1
    strMinValue = str(min_value)
    towrite = ', "Page_' + strMinValue + '":'
    f.write(towrite)
    # print("page ends")
# Click on an element by xpath
# Button = driver.find_element(
#     by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/ul/li[9]')
# Button.click()
f.write('{}}')
f.close()

print(type(MAXVALUE))
# Added sleep option to see if it actually navigates to next page
# time.sleep(5)
# Removed sleep, not needed.
driver.quit()
print("success.")
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

#! Errors and Fixes
# ? Error
# ?      [3028:19420:0130/173925.042:ERROR:device_event_log_impl.cc(215)] [17:39:25.042] USB: usb_device_handle_win.cc:1046 Failed to read descriptor from node connection: A device attached to the system is not functioning. (0x1F)
# ?      [3028:19420:0130/173925.055:ERROR:device_event_log_impl.cc(215)] [17:39:25.055] USB: usb_device_handle_win.cc:1046 Failed to read descriptor from node connection: A device attached to the system is not functioning. (0x1F)
# ?      The next pagination button was accessible due to the scroll top button, now fixed and accessible somehow. 
# ? Fix
# ?      Added line 17 → chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
