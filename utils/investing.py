import steammarket as sm

class Investments:
    def display(self):
        loop = True
        while loop:
            print('――――――――――――――――――――――――――――――――――――――――――')
            print('>>> Investment Information')
            print('――――――――――――――――――――――――――――――――――――――――――')
            print('')
            print(' 0) Exit')
            print(' 1) View Investments')
            print(' 2) Add Investment')
            print(' 3) Remove investment')
            print('')
            action = input('Action: ')
            if action == '0':
                loop = False
                continue
            elif action == '1':
                self.view_items()

    def view_items(self):
        print('――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――')
        print('>>> Current Investments')
        print('――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――')
        print('')
        f_read = open('C:\\Users\\guidenj\\Desktop\\steam\data\\investments.txt', 'r')
        for line in f_read:
            name, amount, orig = line.split(':')
            item = sm.get_csgo_item(name, currency='USD')
            price = float(item["lowest_price"].replace('$',''))*float(amount)
            profit = price - float(orig)*float(amount)
            profit_string = '+$' + str(round(profit, 2))
            if profit < 0:
                profit_string = '-$' + str(round((profit*-1)), 2)
            print('{: >8} {: >2} {: >20} {: >20}'.format(name.ljust(32), 'x'+amount, '$' + str(price), profit_string))
        print('')
        input('ENTER to continue')
