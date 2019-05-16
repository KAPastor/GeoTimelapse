# Tesla Daily Dashboard Market Tracking Bot ====================================
# from InstagramAPI import InstagramAPI
from bs4 import BeautifulSoup
import wget
import requests
import json
import pandas as pd

from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageEnhance
import os, sys
import time
import imageio
from os import listdir
from os.path import isfile, join
import csv
import gpxpy

# ALL YOU NEED FOR THE WHOLE THING
# https://www.strava.com/routes/14426089


run_dir = './DaveSara'


def parsegpx(f):
    points2 = []
    with open(f,'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    dict = {'Timestamp':point.time, \
                        'Latitude': point.latitude, \
                        'Longitude': point.longitude,\
                        'Elevation': point.elevation}
                    points2.append(dict)
    return points2



def CollectData(rundata):


    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=800x800")
    driver = webdriver.Chrome('/Users/kyleanthonypastor/Documents/GitHub/FinDash/chromedriver72',chrome_options=chrome_options )
    # driver.get('https://www.google.ca/maps/')
    # driver.execute_script(""" \
    # var element = document.querySelector("#omnibox-container"); \
    # if (element) \
    #     element.parentNode.removeChild(element); \
    # """)
    # driver.execute_script(""" \
    # var element = document.querySelector(".app-viewcard-strip"); \
    # if (element) \
    #     element.parentNode.removeChild(element); \
    # """)
    # driver.execute_script(""" \
    # var element = document.querySelector("#vasquette"); \
    # if (element) \
    #     element.parentNode.removeChild(element); \
    # """)

    for idx,(index,point) in enumerate(rundata.iterrows()):
        print point
        coordinate_x = str(point['Longitude'])
        coordinate_y = str(point['Latitude'])
        if os.path.isfile(run_dir +  "/output/"+str(idx).zfill(4)+".png"):
            continue

        driver.get('https://www.google.ca/maps/@'+coordinate_y+','+coordinate_x+',18z')
        driver.execute_script(""" \
        var element = document.querySelector("#omnibox-container"); \
        if (element) \
            element.parentNode.removeChild(element); \
        """)
        driver.save_screenshot(run_dir +  "/output/"+str(idx).zfill(4)+".png")
        im = Image.open(run_dir +  "/output/"+str(idx).zfill(4)+".png").convert("RGBA")
        foreground = Image.open("./pin.png").convert("RGBA")
        w, h = im.size
        margin_w, margin_h = foreground.size
        foreground.thumbnail((50,50), Image.ANTIALIAS)

        im.paste(foreground, (375, 350), foreground)
        im.save(run_dir +  "/output/"+str(idx).zfill(4)+".png")


def GenerateGIF():
    images = []
    onlyfiles = [f for f in listdir(run_dir +  "/output/") if isfile(join(run_dir +  "/output/", f))]

    filenames = onlyfiles
    # print filenames
    i=0
    for filename in filenames:
        # if i%5==0:
        print filename
        images.append(imageio.imread(run_dir +  "/output/" + filename))
        i=i+1
    imageio.mimsave(run_dir +  "/Animation.gif", images,duration=0.05)
    print "asfdsf"
    # import ffmpy
    # ff = ffmpy.FFmpeg(inputs={'./output/test2.gif': None},outputs={'./output/test2.mp4': None})
    # ff.run()



def Analyze(input_path,water_color,park_color,beach_color,output_subfolder):
    images = []
    filenames = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    dataset = [['DISTANCE','WATER','PARK','BEACH']]
    i=1.;
    for filename in filenames:
        water_pixels = 0
        park_pixels = 0
        beach_pixels = 0
        total_pixels = 0

        # Collect the data by getting the timestamp
        i=i+1.;
        im = Image.open(input_path + filename)
        width, height = im.size
        # Process every pixel
        for x in range(0,width):
            for y in range(0,height):
                current_color = im.getpixel( (x,y) )
                new_color = (255,255,255)
                total_pixels =total_pixels + 1
                R,G,B,A = current_color
                if (water_color[0][0]<R<water_color[0][1] and \
                    water_color[1][0]<G<water_color[1][1] and \
                    water_color[2][0]<B<water_color[2][1]):
                    new_color = current_color
                    water_pixels = water_pixels + 1
                if (park_color[0][0]<R<park_color[0][1] and \
                    park_color[1][0]<G<park_color[1][1] and \
                    park_color[2][0]<B<park_color[2][1]):
                    new_color = current_color
                    park_pixels = park_pixels + 1
                if (beach_color[0][0]<R<beach_color[0][1] and \
                    beach_color[1][0]<G<beach_color[1][1] and \
                    beach_color[2][0]<B<beach_color[2][1]):
                    new_color = current_color
                    beach_pixels = beach_pixels + 1
                im.putpixel( (x,y), new_color)
        # im.save(input_path + "/debug/" + str(int(i)).zfill(4) + ".png")

        # At this level we collect the datase
        ID = i/248.0*10
        pic_data = [ID,float(water_pixels)/float(total_pixels), \
            float(park_pixels)/float(total_pixels), float(beach_pixels)/float(total_pixels)]
        print pic_data
        dataset.append(pic_data)
        # im.save(input_path + output_subfolder +filename)
        with open(run_dir +  "/dataset.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(dataset)


def PlotData():
    # -*- coding: utf-8 -*-
    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montreal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])

    if __name__ == '__main__':
        app.run_server(debug=True)



# rundata = pd.DataFrame(parsegpx(run_dir + '/Data.gpx'))
# CollectData(rundata)
# GenerateGIF()
# Analyze(run_dir +  "/output/",[[166,168],[217,219],[251,253]],\
#     [[187,199],[235,240],[179,193]],\
#     [[342,244],[342,244],[342,244]],'/')
PlotData()



# driver.implicitly_wait(10) # seconds
# driver.close()

#
# def PostToIG():
#     pass
#     # InstagramAPI = InstagramAPI("tesladailydashboard", "Skiptime1234!@#$")
#     # InstagramAPI.login()  # login
#     # photo_path = './post.jpg'
#     # caption =  datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' -- Tesla (TSLA) Daily Close \n#tesla #teslatouch #teslaarmy #teslaspotting #teslaTeam #teslamodelx #teslagarage #teslamoment #teslathebostonterrier #teslaservicecenter #teslat2 #teslafamily #tesladelivery #Teslainspired #teslamodel #TeslaLive #teslaliving #TeslaTheCat #teslarey #teslasolar #TeslaLisbon #Tesla4me #tesla3 #teslaroadster #teslaconcept #teslaperlwhite #tesladriverlesscars #teslakey #teslamodel3reveal #TeslaOwners'
#     # print(caption)
#     # InstagramAPI.uploadPhoto(photo_path, caption=caption)
# def CollectData():
#     print "Collecting Data"
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--window-size=800x800")
#     driver = webdriver.Chrome('/Users/kyleanthonypastor/Documents/GitHub/FinDash/chromedriver72',chrome_options=chrome_options )
#     driver.get('https://www.google.ca/maps/@43.6437378,-79.379689,16z/data=!5m1!1e1')
#     # driver.implicitly_wait(10) # seconds
#     time.sleep(10)
#     # driver.find_elements_by_css_selector("button.widget-pane-toggle-button")[0].click()
#     driver.execute_script(""" \
#         var element = document.querySelector("#omnibox-container"); \
#         if (element) \
#             element.parentNode.removeChild(element); \
#         """)
#     driver.execute_script(""" \
#         var element = document.querySelector(".app-viewcard-strip"); \
#         if (element) \
#             element.parentNode.removeChild(element); \
#         """)
#     driver.execute_script(""" \
#         var element = document.querySelector("#vasquette"); \
#         if (element) \
#             element.parentNode.removeChild(element); \
#         """)
#
#
#     time.sleep(2)
#
#     # price = driver.find_elements_by_css_selector(".IsqQVc");
#     # element = driver.find_elements_by_css_selector(".knowledge-finance-wholepage__section");
#     # location = element[0].location;
#     # size = element[0].size;
#     driver.save_screenshot("./post.png")
#
#     # x = location['x'];
#     # y = location['y'];
#     # width = location['x']+size['width'];
#     # height = location['y']+size['height'];
#     im = Image.open("./post.png").convert("RGBA")
#     # im = im.crop((int(x), int(y), int(width), int(height)))
#
#     # foreground = Image.open("./logo.png").convert("RGBA")
#     # w, h = im.size
#     # margin_w, margin_h = foreground.size
#     # im.paste(foreground, (w-margin_w, 0), foreground)
#
#     bg = Image.new("RGBA", im.size, (255,255,255))
#     bg.paste(im,im)
#     timestr = time.strftime("%Y%m%d-%H%M%S")
#     timestr_text = time.strftime("%Y-%m-%d\n%H:%M:%S")
#
#
#
#
#
#     # draw = ImageDraw.Draw(bg)
#     # font = ImageFont.truetype(<font-file>, <font-size>)
#     # draw.rectangle(((0, 1095), (305, 1200)), fill=(0,0,0,5))
#     # draw.rectangle(((0, 700), (300, 800)), fill="white")
#
#     # font = ImageFont.truetype("./roboto/Roboto-Bold.ttf", 40)
#     # draw.text((x, y),"Sample Text",(r,g,b))
#     # draw.text((50, 1110),timestr_text,(51,103,214),font=font)
#     # bg = bg.convert("RGB")
#     bg.save("./output/ScotiabankArena/"+timestr+".png")
#
#
#     driver.implicitly_wait(10) # seconds
#     driver.close()
#
#
#
# def FilterPicture(input_path, color_range, output_subfolder):
#     images = []
#     filenames = [f for f in listdir(input_path) if isfile(join(input_path, f))]
#     for filename in filenames:
#         print filename
#         im = Image.open(input_path + filename)
#         width, height = im.size
#         # Process every pixel
#         for x in range(0,width):
#             for y in range(0,height):
#                 current_color = im.getpixel( (x,y) )
#                 R,G,B,A = current_color
#                 # print R,G,B
#                 if not (color_range[0][0]<R<color_range[0][1] and \
#                     color_range[1][0]<G<color_range[1][1] and \
#                     color_range[2][0]<B<color_range[2][1]):
#                     new_color = (255,255,255)
#                     ####################################################################
#                     # Do your logic here and create a new (R,G,B) tuple called new_color
#                     ####################################################################
#                     im.putpixel( (x,y), new_color)
#             # im.save(input_path + "/EXAMPLE/" + str(x).zfill(4) + ".png")
#
#         im.save(input_path + output_subfolder +filename)
#
# def FilterTraffic(input_path, high_color,med_color,low_color,none_color, output_subfolder):
#     images = []
#     filenames = [f for f in listdir(input_path) if isfile(join(input_path, f))]
#     dataset = [['Timestamp','HIGH','MED','LOW','NONE']]
#
#     for filename in filenames:
#         total_traffic_pixels = 0
#         high_pixels = 0
#         med_pixels = 0
#         low_pixels = 0
#         none_pixels = 0
#         # Collect the data by getting the timestamp
#         timestamp = filename.replace('.png','')
#
#         im = Image.open(input_path + filename)
#         width, height = im.size
#         # Process every pixel
#         for x in range(0,width):
#             for y in range(0,height):
#                 current_color = im.getpixel( (x,y) )
#                 new_color = (255,255,255)
#                 R,G,B,A = current_color
#                 if (high_color[0][0]<R<high_color[0][1] and \
#                     high_color[1][0]<G<high_color[1][1] and \
#                     high_color[2][0]<B<high_color[2][1]):
#                     new_color = current_color
#                     high_pixels = high_pixels + 1
#                     total_traffic_pixels = total_traffic_pixels + 1
#                 if (med_color[0][0]<R<med_color[0][1] and \
#                     med_color[1][0]<G<med_color[1][1] and \
#                     med_color[2][0]<B<med_color[2][1]):
#                     new_color = current_color
#                     med_pixels = med_pixels + 1
#                     total_traffic_pixels = total_traffic_pixels + 1
#                 if (low_color[0][0]<R<low_color[0][1] and \
#                     low_color[1][0]<G<low_color[1][1] and \
#                     low_color[2][0]<B<low_color[2][1]):
#                     new_color = current_color
#                     low_pixels = low_pixels + 1
#                     total_traffic_pixels = total_traffic_pixels + 1
#                 if (none_color[0][0]<R<none_color[0][1] and \
#                     none_color[1][0]<G<none_color[1][1] and \
#                     none_color[2][0]<B<none_color[2][1]):
#                     new_color = current_color
#                     none_pixels = none_pixels + 1
#                     total_traffic_pixels = total_traffic_pixels + 1
#                 im.putpixel( (x,y), new_color)
#             # im.save(input_path + "/EXAMPLE/" + str(x).zfill(4) + ".png")
#
#         # At this level we collect the datase
#         pic_data = [timestamp,float(high_pixels)/float(total_traffic_pixels), \
#             float(med_pixels)/float(total_traffic_pixels),\
#             float(low_pixels)/float(total_traffic_pixels),\
#             float(none_pixels)/float(total_traffic_pixels)]
#         print pic_data
#         dataset.append(pic_data)
#         # im.save(input_path + output_subfolder +filename)
#         with open(input_path + output_subfolder + '/dataset.csv', "wb") as f:
#             writer = csv.writer(f)
#             writer.writerows(dataset)
#

#
# # while True:
# #     CollectData()
# # FilterPicture('./output/ScotiabankArena/',[[130,133],[27,31],[31,35]],'/HIGH/')
# # FilterPicture('./output/ScotiabankArena/',[[247,249],[56,58],[55,57]],'/MEDIUM/')
# # FilterPicture('./output/ScotiabankArena/',[[253,256],[149,151],[88,90]],'/LOW/')
# # FilterPicture('./output/ScotiabankArena/',[[83,85],[213,215],[117,119]],'/NONE/')
# FilterTraffic('./output/ScotiabankArena/',[[130,133],[27,31],[31,35]],\
#     [[247,249],[56,58],[55,57]],[[253,256],[149,151],[88,90]],[[83,85],[213,215],[117,119]],'/ALL/')
#
# # GenerateGIF()
