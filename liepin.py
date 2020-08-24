import time
import random
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from io import BytesIO

driver = webdriver.Chrome('D:/lib/chromedriver.exe')
WAIT = WebDriverWait(driver, 10)
url = 'https://www.liepin.com/'

username = '15737937321'
password = '1234567890qwerty'

def get_distance(bg_Image, fullbg_Image):
    #阈值
    threshold = 220

    for i in range(60, bg_Image.size[0]):
        for j in range(bg_Image.size[1]):
            bg_pix = bg_Image.getpixel((i, j))
            fullbg_pix = fullbg_Image.getpixel((i, j))
            r = abs(bg_pix[0] - fullbg_pix[0])
            g = abs(bg_pix[1] - fullbg_pix[1])
            b = abs(bg_pix[2] - fullbg_pix[2])

            if r + g + b > threshold:
                return i

def get_path(distance):
    result = []
    current = 0
    mid = distance * 0.9
    t = 0.1
    v = 0
    while current < (distance):
        if current < mid:
            a = 2 + 2 * random.random()
        else:
            a = -3 - 2 * random.random()
        v0 = v
        v = v0 + a * t
        s = v0 * t + 0.5 * a * t * t
        current += s
        result.append(round(s))
    return result

def start_drag(driver, distance):
    knob = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tc-jpp-img")))
    result = get_path(distance / 2 - 40)
    ActionChains(driver).click_and_hold(knob).perform()

    for x in result:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()

    time.sleep(random.randint(1,10)/10)
    ActionChains(driver).release(knob).perform()

if __name__ == '__main__':
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_css_selector('.operation-title > :nth-child(2)').click()
    driver.find_element_by_css_selector('input[name="login"]').send_keys(username)
    driver.find_element_by_css_selector('input[type="password"]').send_keys(password)
    driver.find_element_by_css_selector('input[value="登 录"]').click()
    
    # 获取滑块按钮
    driver.switch_to.frame('tcaptcha_iframe')
    # 等待加载滑块图片验证码
    time.sleep(3)
    # 获取验证码图片
    img_src = driver.find_element_by_css_selector('.tc-imgarea .tc-bg-img').get_attribute('src')

    # 下载图片
    full_image = requests.get(img_src[:-1] + '0').content
    bg_image = requests.get(img_src[:-1] + '1').content
    slide_image = requests.get(img_src[:-1] + '2').content
   

    # 写入图片
    bg_image_file = Image.open(BytesIO(bg_image))
    full_image_file = Image.open(BytesIO(full_image))
    # bg_image_file.show()
    # full_image_file.show()

    # 计算缺口偏移距离
    dist = get_distance(bg_image_file, full_image_file)
    print('得到距离：%s' % str(dist))
    start_drag(driver, dist)

    # driver.close()

