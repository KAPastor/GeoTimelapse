# Tesla Daily Dashboard Market Tracking Bot ====================================
from InstagramAPI import InstagramAPI
from bs4 import BeautifulSoup
import wget
import requests
import json
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageEnhance
import os, sys
import schedule
import time
import imageio
from os import listdir
from os.path import isfile, join


def PostToIG():
    pass
    # InstagramAPI = InstagramAPI("tesladailydashboard", "Skiptime1234!@#$")
    # InstagramAPI.login()  # login
    # photo_path = './post.jpg'
    # caption =  datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' -- Tesla (TSLA) Daily Close \n#tesla #teslatouch #teslaarmy #teslaspotting #teslaTeam #teslamodelx #teslagarage #teslamoment #teslathebostonterrier #teslaservicecenter #teslat2 #teslafamily #tesladelivery #Teslainspired #teslamodel #TeslaLive #teslaliving #TeslaTheCat #teslarey #teslasolar #TeslaLisbon #Tesla4me #tesla3 #teslaroadster #teslaconcept #teslaperlwhite #tesladriverlesscars #teslakey #teslamodel3reveal #TeslaOwners'
    # print(caption)
    # InstagramAPI.uploadPhoto(photo_path, caption=caption)
def CollectData():
    print "Collecting Data"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=800x800")
    driver = webdriver.Chrome('/Users/kyleanthonypastor/Documents/GitHub/FinDash/chromedriver72',chrome_options=chrome_options )
    driver.get('https://www.google.ca/maps/@43.6612545,-79.4274933,13z/data=!5m1!1e1')
    # driver.implicitly_wait(10) # seconds
    time.sleep(10)
    # driver.find_elements_by_css_selector("button.widget-pane-toggle-button")[0].click()
    driver.execute_script(""" \
        var element = document.querySelector("#omnibox-container"); \
        if (element) \
            element.parentNode.removeChild(element); \
        """)
    time.sleep(2)

    # price = driver.find_elements_by_css_selector(".IsqQVc");
    # element = driver.find_elements_by_css_selector(".knowledge-finance-wholepage__section");
    # location = element[0].location;
    # size = element[0].size;
    driver.save_screenshot("./post.png")

    # x = location['x'];
    # y = location['y'];
    # width = location['x']+size['width'];
    # height = location['y']+size['height'];
    im = Image.open("./post.png").convert("RGBA")
    # im = im.crop((int(x), int(y), int(width), int(height)))

    # foreground = Image.open("./logo.png").convert("RGBA")
    # w, h = im.size
    # margin_w, margin_h = foreground.size
    # im.paste(foreground, (w-margin_w, 0), foreground)

    bg = Image.new("RGBA", im.size, (255,255,255))
    bg.paste(im,im)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    timestr_text = time.strftime("%Y-%m-%d\n%H:%M:%S")





    draw = ImageDraw.Draw(bg)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    # draw.rectangle(((0, 1095), (305, 1200)), fill=(0,0,0,5))
    draw.rectangle(((0, 700), (300, 800)), fill="white")

    font = ImageFont.truetype("./roboto/Roboto-Bold.ttf", 40)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((50, 1110),timestr_text,(51,103,214),font=font)
    bg = bg.convert("RGB")
    bg.save("./output/torontoCore/"+timestr+".jpg")


    driver.implicitly_wait(10) # seconds
    driver.close()



def FilterPicture():
    images = []
    filenames = [f for f in listdir('./output/torontoCore/') if isfile(join('./output/torontoCore/', f))]
    for filename in filenames:
        print filename
        im = Image.open('./output/torontoCore/' + filename)
        width, height = im.size
        # Process every pixel
        for x in range(0,width):
            for y in range(0,height):
                current_color = im.getpixel( (x,y) )
                R,G,B = current_color
                # print R,G,B
                if not (100<R<255 and 0<G<50 and 0<B<50):
                    new_color = (255,255,255)
                    ####################################################################
                    # Do your logic here and create a new (R,G,B) tuple called new_color
                    ####################################################################
                    im.putpixel( (x,y), new_color)
        im.save("./output/torontoCore_test/"+filename)




def GenerateGIF():
    images = []
    onlyfiles = [f for f in listdir('./output/torontoCore_test/') if isfile(join('./output/torontoCore_test/', f))]

    filenames = onlyfiles
    print filenames
    for filename in filenames:
        images.append(imageio.imread('./output/torontoCore_test/' + filename))
    imageio.mimsave('./output/torontoCore_test.gif', images,duration=0.2)

    # import ffmpy
    # ff = ffmpy.FFmpeg(inputs={'./output/test2.gif': None},outputs={'./output/test2.mp4': None})
    # ff.run()

# FilterPicture()
GenerateGIF()
