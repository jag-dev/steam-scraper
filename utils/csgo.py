from bs4 import BeautifulSoup
import requests, json, time
import steammarket as sm

class CSGOItem:
    url = 'https://steamcommunity.com/market/listings/730/'
    cookie = {'steamLoginSecure': 'STEAM LOGIN COOKIE'}
    name = ''

    def __init__(self, name):
        self.name = name.replace(' ', '%20').replace('|', '%7C')
        self.url = ''.join([self.url, self.name.replace('|', '%7C')])

    def __str__(self):
        print('――――――――――――――――――――――――――――――――――――――――――')
        print('>>> ' + self.name.replace('%20', ' ').replace('%7C', '|'))
        try:
            self.stats()
        except (KeyError, TypeError):
            print('[ Success = False, Invalid Item Name ]')
            print('――――――――――――――――――――――――――――――――――――――――――')
            return ''
        print('――――――――――――――――――――――――――――――――――――――――――')
        print('')

        if self.isCase() or self.isSticker():
            item = sm.get_csgo_item(self.name.replace('%20', ' ').replace('%7C', '|'), currency='USD')
            return 'MARKET: ' + item["lowest_price"] + '\n' + 'MEDIAN PRICE: ' + item["median_price"]

        resp = '\n'.join('{0:8} {1:8}'.format(x, y) for x, y in zip(self.market_prices(), self.market_floats()))
        return resp

    def stats(self):
        item = sm.get_csgo_item(self.name.replace('%20', ' ').replace('%7C', '|'), currency='USD')
        print('[ Success = ' + str(item["success"]) + ', Total Volume = ' + item["volume"] + ' ]')

    def lowest_price(self):
        item = sm.get_csgo_item(self.name.replace('%20', ' ').replace('%7C', '|'), currency='USD')
        return item["lowest_price"]

    def isCase(self):
        if self.name.find('Case') != -1 and self.name.find('Hardened') == -1:
            return True
        return False
    def isSticker(self):
        if self.name.find('Sticker') != -1:
            return True
        return False

    def market_prices(self):
        web_page = requests.get(self.url, cookies=self.cookie)
        soup = BeautifulSoup(web_page.text, features="html.parser")
        price_blocks = soup.findAll('span',{'class':'market_listing_price market_listing_price_with_fee'})
        prices = []

        for i in price_blocks:
            str_data = str(i)
            price = str_data.split('\t')
            prices.append(price[6])
        return prices

    def market_floats(self):
        web_page = requests.get(self.url, cookies=self.cookie)
        soup = BeautifulSoup(web_page.text, features="html.parser")
        script_elements = soup.findAll('script')
        floats = []

        for i in script_elements:
            target = str(i)
            if target.find('var g_rgAssets') != -1:
                sep = target.split(';')
                for x in sep:
                    if str(x).find('var g_rgAssets') != -1:
                        asset = str(x).split(',')
                        id = ''
                        link = ''
                        for item in asset:
                            if str(item).find('\"id\":') != -1:
                                id = str(item)
                                id = id.replace('\"id\":\"', '').replace('\"', '')
                            if str(item).find('\"actions\":') != -1:
                                link = str(item)
                                link = link.replace('"actions":[{"link":"', '').replace('\"', '').replace('\\', '').replace('%assetid%', id)

                                item_data = requests.get('https://api.csgofloat.com/?url=' + link)
                                json_resp = json.loads(item_data.text)
                                item_info = json_resp['iteminfo']
                                floats.append(item_info['floatvalue'])
        return floats

class Inventory:
    url = 'http://csgobackpack.net/api/GetInventoryValue/?id='

    def __init__(self, id):
        self.id = id
        self.url = self.url + id

    def checkForSave(self, resp):
        if resp['success'].find('exceeded') == -1:
            with open('C:\\Users\\guidenj\\Desktop\\Desktop\\Util\\py-steam-helper\\data\\inventory.txt', 'r') as save_file:
                with open('C:\\Users\guidenj\\Desktop\\Desktop\\Util\\py-steam-helper\\data\\inventory.txt', 'w') as f_out:
                    for line in save_file:
                        if line.find('Items') != -1:
                            a, b = line.split(':')
                            if b != resp['items']:
                                f_out.write(line.replace(b, resp['items']))
                        if line.find('Value') != -1:
                            a, b = line.split(':')
                            if b != resp['value']:
                                f_out.write(line.replace(b, resp['value']))
                save_file.close()
                f_out.close()
                return True
        else:
            return False

    def __str__(self):
        print('――――――――――――――――――――――――――――――――――――――――――')
        print('>>> Inventory Value')
        print('――――――――――――――――――――――――――――――――――――――――――')
        print('')
        inv_data = requests.get(self.url)
        json_resp = json.loads(inv_data.text)
        if self.checkForSave(json_resp):
            print(' Updated: ' + json_resp['success'])
            print(' Total Items: ' + json_resp['items'])
            print(' Value: $' + json_resp['value'])
            print(' Currency: ' + json_resp['currency'])
        else:
            save_file = open('C:\\Users\\guidenj\\Desktop\\Desktop\\Util\\py-steam-helper\\data\\inventory.txt')
            print(' Updated: false')
            for line in save_file:
                if line.find('Items') != -1:
                    a, b = line.split(':')
                    print(' Total Items: ' + b)
                if line.find('Value') != -1:
                    a, b = line.split(':')
                    print(' Value: $' + b)
        return ''
