from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
from Reminder.reminder_set import reminder
import time,os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def main():  
    driver = webdriver.Chrome(ChromeDriverManager().install())
    try:
        print('Fetching data from the Codeforces Website...')   
        driver.get("https://codeforces.com/enter?back=%2F")
        driver.find_element_by_id('handleOrEmail').send_keys(os.getenv("email_or_username"))
        driver.find_element_by_id('password').send_keys(os.getenv("password"))
        driver.find_element_by_id('password').send_keys(Keys.ENTER)
        time.sleep(4)
        driver.get('https://codeforces.com/contests')
        contest = []
        i=1
        while(1):
            before_text_check = driver.find_element_by_xpath('/html/body/div[6]/div[4]/div[2]/div[1]/div[1]/div[6]/table/tbody/tr['+str(i+1)+']/td[6]').text
            if("Before" in  before_text_check):
                break
            contest_name = driver.find_element_by_xpath('/html/body/div[6]/div[4]/div[2]/div[1]/div[1]/div[6]/table/tbody/tr[' + str(i+1) +']/td[1]').text
            id_contest = driver.find_element_by_xpath('/html/body/div[6]/div[4]/div[2]/div[1]/div[1]/div[6]/table/tbody/tr[' +str(i+1) +']').get_attribute('data-contestid')
            start_time = driver.find_element_by_xpath('/html/body/div[6]/div[4]/div[2]/div[1]/div[1]/div[6]/table/tbody/tr['+str(i+1)+']/td[3]/a').text
            start_time = start_time[:-7]
            start_time = datetime.strptime(start_time, '%b/%d/%Y %H:%M')
            duration = driver.find_element_by_xpath('/html/body/div[6]/div[4]/div[2]/div[1]/div[1]/div[6]/table/tbody/tr['+str(i+1)+']/td[4]').text
            duration = str(duration).split(':')
            end_time = start_time + timedelta(hours = int(duration[0]), minutes = int(duration[1]))
            contest.append({
                "name" : contest_name,
                "start_time" : start_time,
                "end_time" : end_time,
                "id" : id_contest ,
            })
            i=i+1
        i=0
        contest_to_be_deleted = []
        for token in contest:
            driver.get('https://codeforces.com/contestRegistration/'+token['id'])
            if(driver.current_url == 'https://codeforces.com/contests'):
                contest_to_be_deleted.append(i)
                continue
            i = i+1
            driver.find_element_by_xpath('/html/body/div[6]/div[4]/div[2]/form/table/tbody/tr[3]/td/div/input').click()
        print('Fetching of data Complete...')
        print('Now Deleting the Contests that cant be registered...')
        for index in contest_to_be_deleted:
            contest.remove(contest[index])
        print('Deletion complete...')
        # Calling the function to set reminder
        if(len(contest) == 0):
            print("No new Contests...")
            print('Shutting down the program...')
            driver.close()
            return
        print('Starting inserting events in google calendar...')
        for token in contest:
            reminder(token['name'],token['start_time'],token['end_time'])
        print('Finished inserting events in google calendar...')
    except TimeoutException:
        print(TimeoutException)
        driver.close()
    except Exception as e:
        print("ERROR:")
        print(e)
        driver.close()
    driver.close()
    print('Shutting down the program...')
    
if __name__ == '__main__':
    main()