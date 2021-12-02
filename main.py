import datetime
import random
import json
import time, os
import plotly.graph_objs as go
import pandas as pd


jsonFile = os.path.dirname(__file__) + r'/statistics.json'

weekday_d = {   0:['1', 'Monday', 'Montag', 'Mo', 'Mon'],
                1:['2', 'Tuesday', 'Dienstag', 'Tue', 'Tu', 'Di'],
                2:['3', 'Wednesday', 'Mittwoch', 'Wed', 'We', 'Mi'],
                3:['4', 'Thursday', 'Donnerstag', 'Thu', 'Th', 'Do'],
                4:['5', 'Friday', 'Freitag', 'Fri', 'Fr'],
                5:['6', 'Saturday', 'Samstag', 'Sat', 'Sa'],
                6:['0', 'Sunday', 'Sonntag', 'Sun', 'Su', 'So']}
                
def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def selectDificultiy(i: int):
    start = datetime.datetime(2000-i*100, 1, 1)
    end = datetime.datetime(2000+i*100, 1, 1)
    return start, end


def loadData():    
    if os.path.isfile(jsonFile):
        with open(jsonFile) as f:
            return json.load(f) 
    else:
        return []

def dump(data):
    with open(jsonFile, 'w') as f:
        json.dump(data, f, indent=2)

dificultiy = input("Welcome back Jan\nPlease select your dificultiy:")
try:
    dificultiy = int(dificultiy)
except:
    print('Could not assign dificultiy. Select dificultiy = 1')
    dificultiy = 1
startDate, endDate = selectDificultiy(dificultiy)

done = False
while not done:
    # set variables
    correct = False
    startTime = time.time() 

    # guess function
    date = random_date(startDate, endDate)
    guess = input("\nWhat day of the week is the {}.{}.{}?\t".format(
        date.day, date.month, date.year))
    if guess in weekday_d[date.weekday()]:
        print('Correct!')
        correct = True
    else:
        print('Wrong answer. It was a {} ({})'.format(weekday_d[date.weekday()][1], weekday_d[date.weekday()][0]))
    timeTaken = time.time() - startTime

    # save everything to a json file
    data = loadData()
    data.append({"correct":correct, "Time" : timeTaken, 'dificultiy':dificultiy})
    dump(data)
    
    # keep playing question
    keepPlaying = input("Keep plaing? [Y/n]")
    if keepPlaying == 'y' or keepPlaying == 'Y':
        done = False
    else:
        done = True
        print("You did a good job! Have a great Day :)")


data = loadData()
time = [d['Time'] for d in data]
accuracy = [d['correct'] for d in data]
print('\nTime\t\tTotal: {:.2f}s\t\t  Avg.: {:.2f}'.format(sum(time), sum(time)/len(time)))
print('Answers\t\tTotal: {}/{}\t\t  accuracy: {:.2f}'.format(sum(accuracy), len(accuracy), sum(accuracy)/len(accuracy)))


displayResults = input("See statistics? [Y/n]")


if displayResults == 'y' or displayResults == 'Y':

    with open(jsonFile) as f:
        data = json.load(f)

    time = [d['Time'] for d in data]
    accuracy = [d['correct'] for d in data]
    colors = {False: 'red', True: 'darkgreen'}

    df = pd.DataFrame({'y': time, 'x': range(len(time)), 'label': accuracy})

    bars = []
    for label, label_df in df.groupby('label'):
        bars.append(go.Bar(x=label_df.x, y=label_df.y,
                    name=label, marker={'color': colors[label]}))

    fig = go.FigureWidget(data=bars, layout_title_text="Total time: {:.2f}s  \t\tAccuray: {:.2f}%".format(
        sum(time), sum(accuracy)/len(accuracy)))
    fig.show()

