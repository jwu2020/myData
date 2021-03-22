import time
import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


'''
    This script is used to download the user's activity data from Netflix. Tested working with Chrome v77 on windows.

    Input:
    username 
    password
    data_range: integer indication how far back we want to download data for (i.e. 7 = download data for last week; 
                                                                                   1 = today only)
    netflix_name                                                        

    Output:
    JSON file 
            
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
    python -c "from NetflixScrub import download_data; download_data('USERNAME', 'PASSWORD', 2, 'NETFLIXUSER')"

'''


def download_netflix_data(username, password, data_range, netflix_name):

    config = {'netflix_url': 'http://www.netflix.com/login',
              'netflix_activity_url': 'https://www.netflix.com/viewingactivity',
              'user': username,
              'password': password,
              'netflix_id': netflix_name}

    # setting up chrome webdriver in incognito mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    # login to netflix
    driver.get(config['netflix_url'])
    username = driver.find_element_by_id('id_userLoginId')
    username.send_keys(config['user'])
    username.send_keys(Keys.RETURN)
    password = driver.find_element_by_id('id_password')
    password.send_keys(config['password'])
    password.send_keys(Keys.RETURN)
    time.sleep(2)

    # select netflix user
    found_user = False
    users = driver.find_elements_by_class_name('profile-name')
    for index in range(len(users)):
        if config['netflix_id'].lower() == users[index].get_attribute('innerHTML').lower():
            users[index].click()
            found_user = True
            time.sleep(2)
            break

    if found_user is False:
        print("netflix_name does not match any names found. Names are case sensitive.")
        return

    # go to watch history
    driver.get(config['netflix_activity_url'])

    # calculate dates to get data for
    current_date = datetime.date.today()  # YYYY-MM-DD
    last_date = current_date - datetime.timedelta(days=(data_range-1))
    current_date_string = current_date.strftime("%x")  # DD/MM/YY
    video_list = driver.find_elements_by_class_name('retableRow')
    data = {current_date_string: []}

    data_index = 0
    # For each video, look at percentage watched and on what day
    for vid_index in range(len(video_list)):
        video_list = driver.find_elements_by_class_name('retableRow')
        watch_date_string = video_list[vid_index].find_element_by_class_name('col.date.nowrap').get_attribute('innerHTML')
        watch_date = datetime.datetime.strptime(watch_date_string, "%x").date()

        if watch_date < last_date:
            break

        while watch_date != current_date:
            current_date = current_date - datetime.timedelta(days=1)
            current_date_string = current_date.strftime("%x")
            data[current_date_string] = []
            data_index = 0

        # open video
        video_link = video_list[vid_index].find_element_by_class_name('col.title')
        video_link = video_link.find_element_by_xpath(".//a[@href]")
        video_link.click()
        time.sleep(2)

        # find video length and percentage watched
        try:
            video_length = driver.find_element_by_class_name('summary').get_attribute('innerHTML')
            video_watched = driver.find_element_by_class_name('progress-completed').get_attribute('style')
        except NoSuchElementException as e:
            video_length = driver.find_element_by_class_name('duration').get_attribute('innerHTML')
            video_watched = "width: 100%;"

        if video_watched != "width: 100%;":
            first, *middle, last = video_length.split()
            last = last[:-1]
            hrs = int(last)//60
            mins = int(last) % 60
        else:
            hrs, mins = video_length.split()
            hrs = hrs[:-1]
            mins = mins[:-1]

        video_length = str(hrs) + ":" + str(mins)

        data[current_date_string].append({
                'index': data_index,
                'length': video_length,
                'watched': video_watched
        })

        data_index += 1

        # go back
        driver.execute_script("window.history.go(-1)")
        time.sleep(2)

    data_json = json.dumps(data)

    time.sleep(10)
    driver.quit()

    return data_json
