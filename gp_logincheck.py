import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

print('Enter your GlobalProtect VPN IP Address:')
vpn_ip = input()
vpn_url = "https://" + vpn_ip + "/global-protect/login.esp"


def login(username, password):
    """ 
    This is a GlobalProtect Login testing script that takes a user and a pass then logs in with them
    returns either success is login worked or else fail 
    """
    print(username, " - ", password)
    CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              chrome_options=chrome_options
                             )
    driver.get(vpn_url)

    user_field = driver.find_element_by_name('user')
    user_field.clear()
    user_field.send_keys(username)

    password_field = driver.find_element_by_name("passwd")
    password_field.clear()

    password_field.send_keys(password)

    driver.find_element_by_name("ok").click()

    try:
        driver.find_element_by_xpath("//*[@id='dError']/li")
        return "FAIL"
    except:
        return "SUCCESS"
    
    
data = pd.read_csv("vpn_test.csv")

results = []
for user, passw in zip(data['USERNAME'], data['PASSWORD']):
    results.append(login(user, passw))
     
data['RESULT'] = results
data.to_csv("vpn_test_results.csv")
print("SUCCESS, row added")
