import os
import re
from selenium import webdriver
import urllib
from urllib.request import urlretrieve
from random import randint
from time import sleep

def find_similar_images(path, minW, minH, quantity):
    
    images = []
    
    driver = webdriver.Chrome() 
    driver.get('https://yandex.ru/images/')
    sleep(randint(1,2))
    
    driver.find_element_by_css_selector('.icon.icon_type_cbir.input__button').click()
    sleep(randint(1,2))
    
    driver.find_element_by_css_selector(".cbir-panel__file-input")\
                .send_keys(path)
    sleep(15)
    sleep(randint(1,2))
    
    try:
        more_button = driver.find_element_by_css_selector('.similar__thumb_last_yes')
        href = more_button.find_element_by_css_selector('.link_theme_normal').get_attribute('href')
    except:
        return []
    
    driver.get(href)
    sleep(randint(1,2))

    i = 0
    while i < quantity:

        images_on_screen = driver.find_elements_by_css_selector('.serp-item__preview')
        
        for image in images_on_screen:
            
            (w,h) = image.find_element_by_css_selector('.serp-item__meta')\
                    .get_attribute('innerHTML').split('×')
            
            w = re.search(r'\d+', w).group(0)
            h = re.search(r'\d+', h).group(0)
            
            w = int(w)
            h = int(h)
            
            if w >= minW and h >= minH:
            
                image = image.find_element_by_css_selector('.serp-item__link').get_attribute('href')
                
                source = get_image_source(image)
                save_image(source, i)
                i += 1
                
                if i >= quantity:
                    return images

        driver.execute_script("window.scrollTo({}, {})".format(1000*i, 1000*(i+1)))
        sleep(randint(1,2))
        
            
    driver.close()    
    
    return images


def get_image_source(image):

    driver = webdriver.Chrome() 
    driver.get(image)
    sleep(3)

    try:
        roi = driver.find_element_by_css_selector('.sizes')
        source = roi.find_element_by_css_selector('.button2').get_attribute('href')
        driver.close()
        
        return source

    except:
        
        driver.close()
        return 'Falsed'


def save_image(source, i):
    
    try:
        if not os.path.exists('Results'):
            os.mkdir('Results')

        urlretrieve(source, os.path.join('Results', "{}.png".format(i)))
    
    except:
        pass



if __name__ == '__main__':
    
    with open('input.txt', 'r') as f:
        path = f.readline()
        quantity = int(f.readline())
        (minW, minH) = f.readline().split(':')
    
    minW = int(minW)
    minH = int(minH)
        
    images = find_similar_images(path, minW, minH, quantity)
