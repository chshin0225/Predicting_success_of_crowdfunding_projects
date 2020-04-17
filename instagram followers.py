import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['제목', '인스타팔로워수'])

data = pd.read_excel('Wadiz_Sport_Mobility.xlsx')
project_url = list(data['url'])

for url in project_url:
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, 'html.parser')

    title = html.select_one('h2.title').text
    print(title)

    try:
        instagram = html.select_one('ul.social a.instagram')
        instagram_url = instagram.attrs['href']
        print(instagram_url)

        raw_each = requests.get(instagram_url, headers={'User-Agent': 'Mozilla/5.0'})
        html_each = BeautifulSoup(raw_each.text, 'html.parser')
        try:
            followers = html_each.select_one('ul.k9GMp  li:nth-of-type(2)  span.-nal3')
            followers_num = int(followers.attrs['title'])
            print(followers_num)
        except:
            followers_num = 0

    except:
        followers_num = 0

    sheet.append(title, followers_num)

wb.save('Insta followers.xlsx')