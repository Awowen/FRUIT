import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import selenium
import base64
import code
from bs4 import BeautifulSoup

print("-" * 40)
print("-" * 5 + " FRUIT MIDDLEWARE " + "-" * 5)
print("-" * 40)

#facebook = "https://www.messenger.com"
facebook = "https://www.facebok.com"

user_email = "robin.genolet@rgen.io"
user_passwd = base64.b64decode(b'bGliZXJ0cjBsbEZhYjIwMTU=').decode("utf-8")

own_name = "Robin Genolet"
first_name = own_name.split(" ")[0]
target_name = "Axel Uran"
bot_name = "FRUIT"
bot_fb_id = "139284636597150"


driver = webdriver.Chrome("chromedriver_win32\chromedriver.exe")

'''def log_in():
    try:
        print("log_in()")
        mail_field = driver.find_element_by_xpath('//*[@id="email"]')
        passwd_field = driver.find_element_by_xpath('//*[@id="pass"]')
        confirm_buton = driver.find_element_by_xpath('//*[@id="loginbutton"]')
        mail_field.send_keys(user_email)
        passwd_field.send_keys(user_passwd)
        confirm_buton.click()
        return False
    except Exception as e:
        print(e)
        return True'''

def log_in():
    try:
        print("log_in()")
        login_button = driver.find_element_by_name('Continuer en tant que')
        login_button.click()
        return False
    except Exception as e:
        try:
            mail_field = driver.find_element_by_xpath('//*[@id="email"]')
            passwd_field = driver.find_element_by_xpath('//*[@id="pass"]')
            confirm_buton = driver.find_element_by_xpath('//*[@id="loginbutton"]')
            mail_field.send_keys(user_email)
            passwd_field.send_keys(user_passwd)
            confirm_buton.click()
            return False
        except Exception as e:
            pass
    return True

def log_me_in():
        log_in()
def am_i_logged_in():
    try:
        elem = driver.find_element_by_xpath('//*[@id="q"]')
        return True
    except Exception as e:
        return False

def two_fa_auth():
    try:
        #two_fa_field = driver.find_element_by_xpath('//*[@id="approvals_code"]')
        #two_fa_field.send_keys(input('2-FA code: '))
        two_fa_field.send_keys(Keys.ENTER)
    except Exception as e:
        print("Please allow access with your phone.")

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_target_fb_id(target):
    driver.get(facebook)
    search_field = driver.find_element_by_xpath('//*[@id="q"]')
    search_field.send_keys(target)
    search_field.send_keys(Keys.ENTER)
    output = find_between(driver.current_url, "facebook.com/", "?")
    print("get_target_fb_id():", output)
    return output

def send_messenger(target_fd_id, msg):
    driver.get("https://www.messenger.com/t/" + target_fd_id)
    ActionChains(driver).send_keys(msg).send_keys(Keys.ENTER).perform()
    print("done sending")

def connect_messenger(target_fd_id):
    driver.get("https://www.messenger.com/t/" + target_fd_id)
    driver.find_element_by_xpath('//*[@id="u_0_4"]/div/button').click()


driver.get(facebook)
log_me_in()
time.sleep(2)
two_fa_auth()
'''while not am_i_logged_in():
    time.sleep(1)
    log_me_in()
    try:
        continue_button = driver.find_element_by_name('Continuer')
        continue_button.click()
    except Exception as e:
        print("Not logged in yet:", e)
        pass'''
while not am_i_logged_in():
    time.sleep(1)
    log_me_in()

print("Logged in")
# TODO: save cache or something, facebook thinks there is a hack going on ^.^

target_id = get_target_fb_id(target_name)
print("target_id:", target_id)

time.sleep(1)

connect_messenger(target_id)

time.sleep(1)

send_messenger(target_id, "Salut beau gosse")
send_messenger(bot_fb_id, "Hey babe")

div_js_1 = driver.find_element_by_xpath('//*[@id="js_1"]')

source = driver.page_source
soup = BeautifulSoup(source)
messages = soup.find("div", {"id":"js_1"})

msgs = []
for e in messages.find_all('div', {"class":"_1t_p clearfix"}):
    pair = (first_name, e.text[len(first_name):])
    msgs.append(pair)

last_message_p1 = ""
last_message_p2 = ""

def check_new_msg(p):
    global last_message_p1
    global last_message_p2
    if p == 1:
        old_last_m = last_message_p1
    else:
        old_last_m = last_message_p2

    res = []
    i = 0
    last_m = ""
    while old_last_m != last_m:
            i += 1
            last_m = msgs[-i]
            res.append(last_m)
    old_last_m = last_m
    if p == 1:
        last_message_p1 = old_last_m
    else:
        last_message_p2 = old_last_m
    return res

def send_messages(list_msgs, p):
    if p == 1:
        fb_id = target_id
    else:
        fb_id = bot_fb_id
    for msg in list_msgs:
        send_messenger(fb_id, msg[1])

while True:
    m1 = check_new_msg(1)
    print("m1:", m1)
    if m1:
        send_messages(m1, 1)
    m2 = check_new_msg(2)
    print("m2:", m2)
    if m2:
        send_messages(m2, 2)
    time.sleep(2)

code.interact(local=locals())






while True:
    time.sleep(10)
driver.quit()
