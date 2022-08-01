import requests
from bs4 import BeautifulSoup
import json
import time
import random

#TODO: I should swap my casing to match BS4 maybe

def changeDriverPage(driver):
    page = requests.get(URL + "driver/" + driver.strip(".").replace(",","").replace(" ", "_"))
    soup = BeautifulSoup(page.content, "html.parser")

def grabDriverWins(entry):
    #random int to make it less sus
    time.sleep(random.randint(1,4))

    #TODO: the function of this 7 lines up for whatever reason doesnt work? need to find why
    #TODO: theres bound to be a better way to do the following line
    page = requests.get(URL + "driver/" + entry.strip(".").replace(",","").replace(" ", "_"))
    soup = BeautifulSoup(page.content, "html.parser")
    

    statTotals = soup.find_all(class_="tot")
    cupWins = statTotals[0].find_all(class_="col")[2]
    return(cupWins.text.strip())

def findDriverStats(entry):
    #random int to make it less sus
    time.sleep(random.randint(1,4))

    #TODO: the function of this 7 lines up for whatever reason doesnt work? need to find why
    #TODO: theres bound to be a better way to do the following line
    page = requests.get(URL + "driver/" + entry.strip(".").replace(",","").replace(" ", "_"))
    soup = BeautifulSoup(page.content, "html.parser")
    

    statTotals = soup.find_all(class_="tot")
    #cupWins = statTotals[0].find_all(class_="col")[2]
    return(statTotals)
    

#Set url to var to make it easier to call as needed
URL = "https://www.racing-reference.info/"
#placeholder driver for testing
extension = "driver/A_J_Allmendinger/"
page = requests.get(URL + extension)

#soup object
soup = BeautifulSoup(page.content, "html.parser")
#TODO: ''' comments are bad practice. Remove them.
'''
#find driver name, series list, and results tables
driverFind = soup.find(class_="dataCont")
driverName = driverFind.find(("h1"))
seriesResults = soup.find_all(class_="seriesHeader")
statTotals = soup.find_all(class_="tot")

print(driverName.text.strip())
print("")

#finds all series names the driver was in and prints
for sResult in seriesResults:
    seriesElement = sResult.find("h1")
    print(seriesElement.text.strip("Statistics"))
    
print("")
#searches for wins column (unnamed) and prints
for dResult in statTotals:
    winElement = dResult.find_all(class_="col")[2]
    print(winElement.text.strip())


#temp code to test calling data 
xfinitySeries = seriesResults[1].find("h1").text.strip()
xfinityWinStat = statTotals[1].find_all(class_="col")[2]

print(driverName.text.strip() + " has " + xfinityWinStat.text.strip() + " wins in the " + xfinitySeries.strip("Statistics"))

#Attempt to print out total wins for a group of drivers based on a list

driverList = ["Ward Burton"]

print("")
print("Cup wins test:")

for driver in driverList:
    time.sleep(1)
#extension = "driver/" + driver.replace(" ", "_") + "/"

    changeDriverPage(driver)
    soup = BeautifulSoup(page.content, "html.parser")

    driverFind = soup.find(class_="dataCont")
    driverName = driverFind.find(("h1"))
    seriesResults = soup.find_all(class_="seriesHeader")
    statTotals = soup.find_all(class_="tot")

    cupSelector = seriesResults[0].find("h1").text.strip()
    cupWins = statTotals[0].find_all(class_="col")[2]

    print (driver + ": " + cupWins.text.strip())
    time.sleep(1.5)
'''
# testing going to the homepage, finding the most recent race, grabbing drivers, and updating key stats


page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#TODO: Explore if using the "new on the site" tab is actually viable for updating. I dont think it is?
#For now this uses the "2022 season information" tab

#find the latest race link, go to that link
lastCupRaceFind = soup.find_all(class_="seriesMetaLink", href=True)
lastCupRaceLink = "https:" + lastCupRaceFind[0]['href']

page = requests.get(lastCupRaceLink)
soup = BeautifulSoup(page.content, "html.parser")


#find all drivers in the last race, collect their names, collect their wins and print them out
cupDriverArr = []
cupResultTbl = soup.find(class_= "tb race-results-tbl")

cupResultTblList = cupResultTbl.find_all(class_= ["odd", "even"])

#setup for json output, all entrys go into a default "drivers" dictionary
data = {
    "drivers": []
}

with open('sample.json', 'w') as outfile:
    json.dump(data, outfile)

for entry in cupResultTblList:
    entryTbl = entry.find_all(class_="col")
    entryDriver = entryTbl[3].find("a")
    cupDriverArr.append(entryDriver.string)

for entry in cupDriverArr:

    stats = findDriverStats(entry)
    #print(stats)
    cTotalRaces = stats[0].find_all(class_="col")[1]
    cupWins = stats[0].find_all(class_="col")[2]
    cTopFives = stats[0].find_all(class_="col")[3]
    cTopTens = stats[0].find_all(class_="col")[4]


    driverFileAppend = {
        "driver": entry,
        "wins": cTotalRaces.text,
        "top 5s": cTopFives.text,
        "top 10s": cTopTens.text
    }

    with open('sample.json', 'w') as outfile:
        json.append(driverFileAppend, outfile)
    y = json.dumps(driverFileAppend, indent=4, sort_keys=True)
    print(y)
    #print(entry + ": " + grabDriverWins(entry))



