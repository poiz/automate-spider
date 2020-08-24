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
import base64

driver = webdriver.Chrome('D:/lib/chromedriver.exe')
WAIT = WebDriverWait(driver, 10)
url = 'https://passport.zhaopin.com/login'

username = '13127913279'
password = 'abc123_'

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
    mid = distance * 0.8
    t = 0.2
    v = 2
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
    knob = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "DIV.geetest_slider_button")))
    result = get_path(distance - 8)
    ActionChains(driver).click_and_hold(knob).perform()

    for x in result:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=random.randint(-10,10)).perform()

    time.sleep(random.randint(1,10)/10)
    ActionChains(driver).release(knob).perform()

def get_canvas_bg(js):
    # 下面的js代码根据canvas文档说明而来
    # js = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
    # 执行 JS 代码并拿到图片 base64 数据
    im_info = driver.execute_script(js)      # 执行js文件得到带图片信息的图片数据
    im_base64 = im_info.split(',')[1]        # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)   # 转为bytes类型
    return Image.open(BytesIO(im_bytes))

if __name__ == '__main__':
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_css_selector('.zppp-panel-qrcode-bar__triangle').click()
    driver.find_element_by_css_selector('.zppp-panel-tabs > :nth-child(2)').click()
    driver.find_element_by_css_selector('input[placeholder="用户名/手机号/邮箱"]').send_keys(username)
    driver.find_element_by_css_selector('input[placeholder="密码"]').send_keys(password)
    driver.find_element_by_css_selector('.zppp-submit').click()
    
    # 获取滑块按钮
    # 等待加载滑块图片验证码
    time.sleep(3)

    # 写入图片
    bg_image_file = get_canvas_bg('return document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0].toDataURL("image/png");')
    full_image_file = get_canvas_bg('return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");')
    # bg_image_file.show()
    # full_image_file.show()

    # # 计算缺口偏移距离
    dist = get_distance(bg_image_file, full_image_file)
    print('得到距离：%s' % str(dist))
    start_drag(driver, dist)

    # driver.close()

