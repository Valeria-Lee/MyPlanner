from datetime import datetime, timedelta, time
from pyfiglet import Figlet
from termcolor import cprint
from time import sleep
import random
import csv

class Day:
    def __init__(self, day_name, activities=[], start_time=[], end_time = []):
        self.day_name = day_name
        self.activities = []
        self.start_time = []
        self.end_time = []

    # de esta forma, llenamos activities y time.
    def fill_schedule(self):
        with open('schedule.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            data = list(reader)
            for row in data:
                if row[0] == self.day_name:
                    self.activities.append(row[1])
                    self.start_time.append(row[2])
                    self.end_time.append(row[3])
            # print(self.activities)

    def get_schedule(self) -> None:
        print(f'{self.day_name}')
        for i in range(len(self.activities)):
            print(f'{self.start_time[i]} - {self.end_time[i]} -> {self.activities[i]}')

    def consult_act(self, hour):
        hour_to_search = time(int(hour[0:2]), int(hour[3:5]))

        for i in range (len(self.start_time)):
            start_hour = int(self.start_time[i][0:2]) # hour.
            start_min = int(self.start_time[i][3:5]) # seconds.
            start_range = time(start_hour, start_min)

            end_hour = int(self.end_time[i][0:2]) # hour.
            end_min = int(self.end_time[i][3:5]) # seconds.
            end_range = time(end_hour, end_min)

            if start_range < hour_to_search < end_range:
                print(f'{start_range} < {hour_to_search} < {end_range}')

        print(self.activities[i-1])


def get_hour(current_time) -> str:
    minutes = (current_time.minute if current_time.minute > 10 else '0' + str(current_time.minute)) # menos de dos cifras, se anade un cero al inicio.
    hour = f'{current_time.hour}:{minutes}'
    print(hour)
    return hour

def get_day(current_time) -> str:
    day = ''
    day_num = datetime.weekday(current_time) # retorna un numero del 0 - 6.

    match day_num:
        case 0:
            day = 'Monday'
        case 1:
            day = 'Tuesday'
        case 2:
            day = 'Wednesday'
        case 3:
            day = 'Thursday'
        case 4:
            day = 'Friday'
        case 5:
            day = 'Saturday'
        case 6:
            day = 'Sunday'

    print(day)
    return day

def init_days() -> list:
    monday = Day('Monday')
    tuesday = Day('Tuesday')
    wednesday = Day('Wednesday')
    thursday = Day('Thursday')
    friday = Day('Friday')

    days = [monday, tuesday, wednesday, thursday, friday]

    i:int = 0

    while i < len(days):
        # print(f'Filling schedule: {days[i].day_name}...')
        days[i].fill_schedule()
        i+=1

    return days

def gimme_hobbie():
    hobbies = []
    hobbie_materials = []

    with open('hobbie_ideas.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        for row in data:
            hobbies.append(row[0])
            hobbie_materials.append(row[1])

    chosen_index = random.randint(0,6)
    chosen_hobbie = hobbies[chosen_index]
    needed_materiales = hobbie_materials[chosen_index]

    return [chosen_hobbie, needed_materiales]

def get_menu():
    day_object = None

    current_time = datetime.now()
    # hour = get_hour(current_time)
    hour = '18:20'
    # day = get_day(current_time)
    day = 'Monday' # Para probar, recuerda que no tienes del finde.

    days = init_days()

    f = Figlet(font='alligator')
    print(f.renderText('planner'))

    decoration = "* " * 16

    using = True

    for d in days:
        if d.day_name == day:
            day_object = d

    while using:

        cprint(decoration + " Select an option: " + decoration, "black", "on_light_red")

        cprint("| (1) Consult schedule | (2) Consult activity | (3) Get a hobbie | (4) Quit", "white", "on_yellow")

        opt = int(input())

        match opt:
            case 1:
                d.get_schedule()
            case 2:
                day_object.consult_act(hour)
            case 3:
                print(gimme_hobbie())
            case 4:
                cprint("-> Quitting...", "white", "on_red")
                using = False

        sleep(0.5)

def main():
    get_menu()


if __name__ == '__main__':
    main()
