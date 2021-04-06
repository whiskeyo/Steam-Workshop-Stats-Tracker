import os
import platform
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://steamcommunity.com/sharedfiles/filedetails/?id=314892291"

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')

def get_data(URL):
    result = requests.get(URL)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    return soup.find("table", {"class": "stats_table"})

def parse_table(table):
    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    for row in data:
        row[0] = int(row[0].replace(',', ''))
        row.reverse()

    return data

def print_since_started(date, starting, current):
    print("------------------------------------------------------------")
    print("Gains since starting scraping (", date, ")")
    print("New visitors:    ", current[0][1] - starting[0][1])
    print("New subscribers: ", current[1][1] - starting[1][1])
    print("New favorites:   ", current[2][1] - starting[2][1])

def print_diff(previous, current):
    # There are 3 different values: unique visitors, current subs and favorites
    # We want to compare data from previous fetch with the current fetch so we
    # can print differences. Each "row" has 2 "columns"
    print("------------------------------------------------------------")
    for i in range(0,3):
        if previous[i][1] != current[i][1]:
            diff = current[i][1] - previous[i][1]
            if diff >= 0:
                diff = "+" + str(diff)

            print("{: <20} {: <20} ({})".format(current[i][0], current[i][1], diff))
        else:
            print("{: <20} {: <20} (+0)".format(current[i][0], current[i][1]))
                
def print_graph(records, height=15, width=60):
    # Map [visitors, subs, favorites] to [zeroes, favs, visitors, subs]
    mapped_records = [ [height - sum(x), x[2], x[0], x[1]] for x in records ]
    # print("Mapped: ", mapped_records)
    string_records = [] 
    for entry in mapped_records:
        new_entry = []
        for i in range(entry[0]):
            new_entry.append(' ')
        for i in range(entry[1]):
            new_entry.append('f')
        for i in range(entry[2]):
            new_entry.append('v')
        for i in range(entry[3]):
            new_entry.append('s')

        string_records.append(new_entry)

    # print("String: ", string_records)

    print("---------- GRAPH OF LAST 60 MINUTES OF ACTIVITY ------------")
    for row in range(0, height):
        for col in range(0, width):
            print(string_records[col][row], end='')

        print("")

    print("------------------------------------------------------------")
    print("oldest                                                newest")
    print("event                                                  event")

def print_interval(seconds):
    previous_data = []
    current_data = parse_table(get_data(URL))
    
    last_60_records = [ [0, 0, 0] for i in range(60) ]
    all_records = 60

    starting_data = current_data
    starting_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        while True:
            previous_data = current_data
            current_data = parse_table(get_data(URL))

            differences = [
                current_data[0][1] - previous_data[0][1], # visitors
                current_data[1][1] - previous_data[1][1], # subs
                current_data[2][1] - previous_data[2][1]  # favorites
            ]
            last_60_records.append([max(val, 0) for val in differences])
            last_60_records = last_60_records[-all_records:]

            current_time = datetime.now()
            fetch_datetime = current_time.strftime("%d/%m/%Y %H:%M:%S")
            date = current_time.strftime("%d-%m-%Y")

            # Save data as: datetime | new visitors | new subs | new favs
            with open(f"{date}.txt", "a+") as f:
                append_data = current_time.strftime("%H:%M") + "; " + \
                    str(differences[0]) + "; " + \
                    str(differences[1]) + "; " + \
                    str(differences[2]) + "\n"
                f.write(append_data)

            clear()
            print("-------------------------------------Last data fetch--------")
            print("Jumps Training Statistics           ", fetch_datetime)    
            print_diff(previous_data, current_data)
            print_since_started(starting_time, starting_data, current_data)
            print_graph(last_60_records, height=15)
            time.sleep(seconds)
    except KeyboardInterrupt:
        pass

print_interval(60)