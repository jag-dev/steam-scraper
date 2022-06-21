from bs4 import BeautifulSoup
from datetime import date
from utils.csgo import CSGOItem, Inventory
from utils.investing import Investments
import requests, json
"""
Created on Sat Dec 12 20:57:10 2020

@author: JaG
"""
loop = True
while (loop):
    print('――――――――――――――――――――――――――――――――――――――――――')
    print('>>> Select an action')
    print('――――――――――――――――――――――――――――――――――――――――――')
    print('')
    print(' 0) Exit program')
    print(' 1) Search item')
    print(' 2) Inventory info')
    print(' 3) Investment Center')
    print('')
    action = input('Action: ')
    if action == '0':
        loop = False
        continue
    elif action == '1':
        name = input('Enter item: ')
        item = CSGOItem(name)
        print(item)
        print('')
    elif action == '2':
        inv = Inventory('76561198103639441')
        print(inv)
    elif action == '3':
        investments = Investments()
        investments.display()
    input('ENTER to continue')
