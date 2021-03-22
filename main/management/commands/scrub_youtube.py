import time
import datetime
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

'''
    This script is used to download the user's activity data from youtube. Tested working with Chrome v77 on windows.

    Input:
    username 
    password
    data_range: integer indication how far back we want to download data for (i.e. 7 = download data for last week; 
                                                                                   1 = today only)

    Output:
    JSON file:
            
        {
            "date_string": [
                {
                    "index": 0, 
                    "length": "2:31", 
                    "watched": "width: 10%;"
                }
            ], 
            "date_string": [
                {
                    "index": 0, 
                    "length": "2:31", 
                    "watched": "width: 33%;" 
                }, 
                {
                    "index": 1, 
                    "length": "12:01", 
                    "watched": "width: 10%;"
                }
            ]
        }

    run in console:
    python -c "from scrub_youtube import download_youtube_data; download_youtube__data('USERNAME', 'PASSWORD', 2)"

'''


def download_youtube_data(username, password, data_range):

    config = {'youtube_url': 'http://www.youtube.com/account',
              'user': username,
              'password': password,
              'youtube_activity_url': 'https://myactivity.google.com/activitycontrols/youtube?utm_medium=web&utm_source=youtube'}

    # setting up chrome webdriver in incognito mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    # login to youtube
    driver.get(config['youtube_url'])
    username = driver.find_element_by_id('identifierId')
    username.send_keys(config['user'])
    username.send_keys(Keys.RETURN)
    time.sleep(3)
    password = driver.find_element_by_name('password')
    password.send_keys(config['password'])
    password.send_keys(Keys.RETURN)
    time.sleep(2)

    # go to myActivity page
    driver.get(config['youtube_activity_url'])

    # For each day, find the videos watched and percentages watch for
    date = datetime.date.today()  # YYYY-MM-DD
    data = {}
    for day in range(data_range):
        date_string = date.strftime("%Y%m%d")  # YYYYMMDD
        videos = driver.find_elements_by_xpath("//c-wiz[@data-date='" + date_string + "']//div[@class='OUPWA']")

        data[date_string] = []
        for index in range(len(videos)):
            vid_length = videos[index].find_element_by_xpath(".//div[@class='bI9urf']").get_attribute("innerHTML")

            try:
                vid_watched = videos[index].find_element_by_xpath(".//div[@class='HmLFgd']").get_attribute("style")
            except NoSuchElementException:
                vid_watched = "width: 100%;"

            data[date_string].append({
                        'index': index,
                        'length': vid_length,
                        'watched': vid_watched
                    })

        # increment date
        date = date - datetime.timedelta(days=1)

    data_json = json.dumps(data)
    driver.quit()
    return data_json
