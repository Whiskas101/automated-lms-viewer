from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# this was made horribly.
# but it works!
# will also download SOME of the ppts mentioned in the thingy


EMAIL = input('Enter MyDy Email : ')
PASSWORD = input('Password : ')

target_url = 'http:\\mydy.dypatil.edu'
browser = webdriver.Chrome()
browser.maximize_window()

browser.get(target_url)

login_email_form = browser.find_element(By.ID, "username")
login_email_form.send_keys(EMAIL)

next_button = browser.find_element(By.ID, "loginbtn")
next_button.click()

login_passw_form = browser.find_element(By.ID, "password")
login_passw_form.send_keys(PASSWORD)

next_button = browser.find_element(By.ID, "loginbtn")
next_button.send_keys(Keys.ENTER)

#WAIT
wait = WebDriverWait(browser, 25, 1)

subjects = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'launchbutton')))


dashboard_window = browser.current_window_handle
# windows = browser.window_handles

#Storing Links to each subject page 
SUBJECT_LINKS = []
for subject in subjects:
    SUBJECT_LINKS.append(subject.get_attribute("href"))

dbms_id = "5197"
link_to_dbms = "http://mydy.dypatil.edu/rait/course/view.php?id=5197"
SUBJECT_LINKS.append(link_to_dbms)

#going to EACH subject page, and storing each "activity" link
final_activity_links = []
for link in SUBJECT_LINKS:
    browser.get(link)
    Activities = browser.find_elements(By.CLASS_NAME, "activityinstance")
    
    print("There are ",len(Activities), " items here")
    activityLinks = []
    for activity in Activities:
        activity2 = activity.find_element(By.TAG_NAME, 'a')
        link = activity2.get_attribute('href')
        activityLinks.append(link)

    

    final_activity_links.extend(activityLinks)
    

print("LENGTH : ", len(final_activity_links))

for link in final_activity_links:
    browser.get(link)







