from fileinput import FileInput
import telegram_bot.handlers.DB as DB
from datetime import datetime


class CountResources:

    def __init__(self, data, m=None):
        self.data = data
        self.mouth = (m if m else str(datetime.now().strftime("%m")))
        self.year = {'01': DB.m01, '02': DB.m02, '03': DB.m03, '04': DB.m04, '05': DB.m05, '06': DB.m06, '07': DB.m07,
                     '08': DB.m08, '09': DB.m09, '10': DB.m10, '11': DB.m11, '12': DB.m12}
        self.past_data = (self.year['0' + str(int(self.mouth) - 1)] if int(self.mouth) > 1 else self.year['12'])
        self.tot = 0
        self.gas_cost = 0
        self.water_cost = 0
        self.el_cost = 0

    def run(self):
        self.gas()
        print(self.gas_cost)
        self.water()
        print(self.water_cost)
        self.el()
        print(self.el_cost)
        self.tot = self.gas_cost + self.water_cost + self.el_cost
        print(f'You need to pay {round(self.tot,2)} rubles for resources')

    def gas(self, add=0):
        '''gas counting'''
        self.gas_cost = round(self.past_data['gas_rub'] - self.data['gas_rub'] + add, 2)

    def water(self):
        '''water counting'''
        cube = self.data['water'] - self.past_data['water']
        self.water_cost = (cube * DB.WATER) + (cube * DB.WATER_DISPOSAL)

    def el(self):
        '''electricity counting two tariff'''
        el = self.data['el1'] + self.data['el2']
        self.el_cost = round((el - self.past_data['el']) * DB.ELECTRICITY, 2)

    def write_to_file(self):
        '''write to file'''
        str_new = f"m{self.mouth} = {{'gas_num': {self.data['gas_num']}, 'gas_rub': {self.data['gas_rub']}, " \
                  f"'water': {self.data['water']}, 'el': {self.data['el1'] + self.data['el2']}}} "
        # print(str_new)
        with FileInput('handlers/DB.py', inplace=True, backup=f'{datetime.now()}.bak') as file:
            for line in file:
                line = line.rstrip()  # remove trailing (invisible) space
                print(str_new if line.startswith(f'm{self.mouth}') else line)  # stdout is redirected to the file
        # # os.unlink(filename + '.bak')  # remove the backup on success


if __name__ == '__main__':
    data = {'gas_num': 2513, 'gas_rub': 3089.78, 'water': 221, 'el1': 6700, 'el2': 34}
    count = CountResources(data=data, m='08')
    count.run()
