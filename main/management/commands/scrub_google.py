import time
import datetime
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

'''
    This script is used to download the user's activity data from google. Tested working with Chrome v77 on windows.

    Input:
    username 
    password
    data_range: integer indication how far back we want to download data for (i.e. 7 = download data for last week; 
                                                                                   1 = today only)

    Output :
    JSON file example:

        {
            "date_string": [
                {
                    "index": 0, 
                    "time": "8:15AM", 
                    "hits": 3
                }
            ], 
            "date_string": [
                {
                    "index": 0, 
                    "time": "9:01PM", 
                    "hits": 2
                }, 
                {
                    "index": 1, 
                    "time": "9:04PM", 
                    "hits": 4 
                }
            ]
        }

    run in console:
    python -c "from scrub_google import download_google_data; download_google_data('USERNAME', 'PASSWORD', 2)"

'''


def download_google_data(username, password, data_range):
    config = {'youtube_url': 'http://www.youtube.com/account',
              'user': username,
              'password': password,
              'google_activity_url': 'https://myactivity.google.com/item?product=11%2C19'}

    # setting up chrome webdriver in incognito mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    # login to youtube
    driver.get(config['youtube_url'])
    username = driver.find_element_by_id('identifierId')
    username.send_keys(config['user'])
    username.send_keys(Keys.RETURN)
    time.sleep(4)
    password = driver.find_element_by_name('password')
    password.send_keys(config['password'])
    password.send_keys(Keys.RETURN)
    time.sleep(3)

    # go to myActivity page
    driver.get(config['google_activity_url'])

    # starting from today's date -> data_range, find what times searches were made and how many were made
    date = datetime.date.today()  # YYYY-MM-DD
    data = {}
    data_range += 1

    for day in range(data_range):
        date_string = date.strftime("%Y%m%d")  # YYYYMMDD
        data[date_string] = []

        timestamps_xpath = "//c-wiz[@data-date='" + date_string + "']//div[contains(@class, 'H3Q9vf') and contains(@class, 'XTnvW')]"
        timestamps = driver.find_elements_by_xpath(timestamps_xpath)
        print(timestamps)
        # no data for this day
        if len(timestamps) == 0:
            break

        current_timestamp = timestamps[0].get_attribute("innerHTML")[:8]
        json_index = 0
        search_hits = 0
        for index in range(len(timestamps)):
            if timestamps[index].get_attribute("innerHTML")[:8] != current_timestamp:
                data[date_string].append({
                    'index': json_index,
                    'time': current_timestamp,
                    'hits': search_hits
                })

                json_index += 1
                current_timestamp = timestamps[index].get_attribute("innerHTML")[:8]
            else:
                search_hits += 1

        # increment date
        date = date - datetime.timedelta(days=1)

    data_json = json.dumps(data)
    print(data_json)
    driver.quit()
    return data_json
