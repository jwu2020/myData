import time
import datetime
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from django.conf import settings
import zipfile

'''
    This script is used to download the user's activity data from facebook. Tested working with Chrome v77 on windows.
    
    Input:
    username 
    password
    download_path: where the output will be stored
    data_range: integer indication how far back we want to download data for (i.e. 7 = download data for last week; 
                                                                                   1 = today only)
    
    Output:
    path of the zip file which contains activity data in JSON format
    
    run in console:
    python -c "from FacebookScrub import download_data; download_data('USERNAME', 'PASSWORD', 'C:\\Users\\USER\\Downloads', 1)"

'''


# TODO: Get fb ID

def download_data(username, password, download_path, data_range):

    config = {'facebook_url': 'https://www.facebook.com',
              'user': username,
              'password': password,
              'facebookInfo_url': 'https://www.facebook.com/settings?tab=your_facebook_information'}

    # setting up chrome webdriver in incognito mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    pref = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        }
    chrome_options.add_experimental_option("prefs", pref)
    driver = webdriver.Chrome(options=chrome_options)

    # login to facebook
    driver.get(config['facebook_url'])
    try:
        username = driver.find_element_by_id('email')
        password = driver.find_element_by_id('pass')
    except NoSuchElementException:
        input_area = driver.find_elements_by_css_selector('input.inputtext._55r1._6luy')

        print(input_area)

        username = input_area[0]
        password = input_area[1]

    username.send_keys(config['user'])
    password.send_keys(config['password'])
    password.submit()
    time.sleep(1)  # Let the user actually see something!

    # go to download information page
    driver.get(config['facebookInfo_url'])
    download_your_information = driver.find_element_by_id('u_0_8')
    download_your_information.click()
    time.sleep(2)

    # selecting what data to download
    html = driver.find_element_by_tag_name('html')
    buttons = driver.find_elements_by_css_selector('button._1gcq._29c-._1gco._5e9w')

    check = [0, 2, 3, 7, 8, 17]  # checkboxes

    time.sleep(1)
    for i in range(23):
        if i not in check:
            try:
                buttons[i].click()
            except:
                html.send_keys(Keys.PAGE_DOWN)
                time.sleep(3)
                buttons[i].click()

    # identify the start and end dates
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=data_range)
    print(today)   # YYYY-MM-DD
    print(start_date)

    driver.execute_script("window.scrollTo(0, 0)")
    # html.send_keys(Keys.PAGE_UP)
    time.sleep(1)

    # Format: JSON
    driver.find_element_by_css_selector('div._3-9a.uiPopover._6a').click()
    driver.find_elements_by_css_selector('li._54ni.__MenuItem')[1].click()

    # Date range:
    all_of_my_data = driver.find_elements_by_css_selector('span._3-9a._5hq9')[0].click()
    dropdown_month = driver.find_elements_by_css_selector('div._2-co.uiPopover._6a._6b')
    dropdown_month[0].click()
    time.sleep(1)
    dropdown_options = driver.find_elements_by_css_selector('span._54nh')
    dropdown_options[start_date.month+1].click()  # select starting month

    # select start year (end year is set by default to current year)
    dropdown_year = driver.find_element_by_css_selector('div._2-cq.uiPopover._6a._6b')
    dropdown_year.click()
    time.sleep(1)
    dropdown_options = driver.find_elements_by_css_selector('span._54nh')
    print(dropdown_options.__sizeof__())
    if today.year == start_date.year:
        dropdown_options[14].click()
    else:
        dropdown_options[15].click()

    day_options = driver.find_elements_by_css_selector('span._5hq1')
    day_options[start_date.day-1].click()  # select starting day

    driver.find_element_by_css_selector('button._4jy0._4jy3._4jy1._51sy.selected._42ft').click()
    driver.find_element_by_css_selector('div._43rl').click()  # create file

    print("Waiting for download file to be generated")
    time.sleep(90*data_range)  # wait 2 * n (no. of days) minutes
    driver.find_elements_by_css_selector('div._4jq5')[1].click()  # click on available copies

    dl_success = False
    while dl_success is False:
        buttons = driver.find_elements_by_class_name('_43rm')
        try:
            print(buttons[2].get_attribute('innerHTML'))
            if buttons[2].get_attribute('innerHTML') == 'Download':
                dl_success = True
            else:
                time.sleep(20 * data_range)
                driver.execute_script("window.history.go()")
                print("refreshing")
        except:
            time.sleep(20 * data_range)
            driver.execute_script("window.history.go()")
            print("refreshing")

    time.sleep(5)
    buttons[2].find_element_by_xpath('..').click()
    data_range = data_range + 1
    time.sleep(10 * data_range)  # wait for file to finish downloading
    driver.quit()

    # Download
    for file in os.listdir(os.path.expanduser(download_path)):
        if file.startswith("facebook") and file.endswith(".zip"):
            return os.path.join(download_path, file)


if __name__ == "main":
    download_data("j.esswu@hotmail.com", "halloffame", "~/Downloads", 1)