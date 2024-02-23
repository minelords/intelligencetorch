import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

def checkpoint(url): 
    # 1. explorer settings
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # 2. driver
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    print("start...\nplease wait a 20 second...")
    time.sleep(20) #为什么不用隐性或者显性等待呢，因为都有问题，所以只能自己修改sleep时间
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    body=soup.find("div",{"id":"txt2img_checkpoints_cards","class":"extra-network-cards"})
    tag=body.find_all("span",{"class":"name"})
    driver.quit()
    point=[]
    for t in tag:
        point.append(t.get_text())
    return point

if __name__=="__main__":
    url='http://119.23.213.95:8001'
    print(checkpoint(url))    
