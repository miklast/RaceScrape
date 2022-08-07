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
    time.sleep(random.randint(2,7))

    #TODO: the function of this 7 lines up for whatever reason doesnt work? need to find why
    #TODO: theres bound to be a better way to do the following line
    page = requests.get(URL + "driver/" + entry.strip(".").replace(",","").replace(" ", "_"))
    soup = BeautifulSoup(page.content, "html.parser")
    

    statTotals = soup.find_all(class_="tot")
    cupWins = statTotals[0].find_all(class_="col")[2]
    return(cupWins.text.strip())

def findDriverStats(entry):
    #random int to make it less sus
    time.sleep(random.randint(1,8))

    #TODO: the function of this 7 lines up for whatever reason doesnt work? need to find why
    #TODO: theres bound to be a better way to do the following line

    #TODO: this code does not work for some names. Extra testing is needed to fix
    page = requests.get(URL + "driver/" + entry.strip(".").replace(",","").replace(" ", "_"))
    soup = BeautifulSoup(page.content, "html.parser")
    

    statTotals = soup.find_all(class_="tot")
    #print(statTotals)
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

# Code to collect all driver names from standings pages. 
#TODO: find out if this includes everyone

standYr = 2022
driverList = []

for year in range(1):
    time.sleep(random.randint(2,10))
    standExt = "standings/" + str(standYr) + "/W/"
    print(URL + standExt)
    page = requests.get(URL+ "standings/" + str(standYr) + "/W/")
    soup = BeautifulSoup(page.content, "html.parser")

    standResultTbl = soup.find(class_= "tb standingsTbl")
    cupDriverList = standResultTbl.find_all(class_= ["odd", "even"])

    for entry in cupDriverList:
        entryTbl = entry.find_all(class_="col")
        entryDriver = entryTbl[1].find("a")


        if entryDriver.string in driverList:
            print(entryDriver.string)
            continue
        else:
            driverList.append(entryDriver.string)
    
    standYr+=1

print(driverList)

# testing going to the homepage, finding the most recent race, grabbing drivers, and updating key stats


page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#TODO: Explore if using the "new on the site" tab is actually viable for updating. I dont think it is?
#For now this uses the "2022 season information" tab

#find the latest race link, go to that link
lastCupRaceFind = soup.find_all(class_="seriesMetaLink", href=True)
lastCupRaceLink = "https:" + lastCupRaceFind[0]['href']

#page = requests.get(lastCupRaceLink)
page = requests.get("https://www.racing-reference.info/race-results/1998_Daytona_500/W/")
soup = BeautifulSoup(page.content, "html.parser")


#find all drivers in the last race, collect their names, collect their wins and print them out
cupDriverArr = []
cupResultTbl = soup.find(class_= "tb race-results-tbl")

cupResultTblList = cupResultTbl.find_all(class_= ["odd", "even"])

#setup for json output, all entries go into a default "drivers" dictionary
data = {}

#with open('sample.json', 'w') as outfile:
    #json.dump(data, outfile)

for entry in cupResultTblList:
    entryTbl = entry.find_all(class_="col")
    entryDriver = entryTbl[3].find("a")
    cupDriverArr.append(entryDriver.string)

eInt = 0


for entry in cupDriverArr:

    #The follwing function is broken, figure out why
    #stats = findDriverStats(entry)

    time.sleep(random.randint(2,10))
    page = requests.get(URL + "driver/" + entry.strip(".").replace(",","").replace(" ", "_"))
    soup = BeautifulSoup(page.content, "html.parser")

    statTbl = soup.find_all(class_= ["tb"])
    tbFind = statTbl[1].find_all(class_= ["odd", "even"])

    
    stats = soup.find_all(class_="tot")

    #old way of finding the last year
    #lastYrTest = stats[0].previous_sibling.find_all(class_="col")[0]


    #Checks to see if a driver competed in the first listed year via their "X of Y" races
    #test example is Kyle Busch, 2003 cup was 0 of 36 and was not his first cup year
    #TODO: Fix the issue that requires the use of an extra variable outside the loop
    yrStartTest = 0
    for x in tbFind:
        if (int(tbFind[yrStartTest].find_all(class_="col")[2].text[:3]) == 0):
            yrStartTest+=1
            continue
        else:
            cYrFirst = tbFind[yrStartTest].find_all(class_="col")[0].text.replace("of 36", '').strip()
            break

    
    yrEndTest = len(tbFind)-1

    #This goes and checks the end year for any starts
    for x in tbFind:
        if (int(tbFind[yrEndTest].find_all(class_="col")[2].text[:3]) == 0):
            yrEndTest-=1
            continue
        else:
            cYrLast = tbFind[yrEndTest].find_all(class_="col")[0].text.replace("of 36", '').strip()
            break

    champCount = 0
    counter = 0


    for x in tbFind:

        try:
            cmpCheck = tbFind[counter].find_all(class_="col")[10].text
            cmpPrintTest=tbFind[counter].find_all(class_="col")[10]

            if (int(cmpCheck) == 1):
                champCount+=1
                counter+=1
                continue
            else:
                counter+=1
                continue
            
        except:
            print("bad unicode prob " + entry)
            print(counter)
            print(tbFind[counter-1].find_all(class_="col"))
            counter+=1
            continue

    



    #I abstracted myself too far to get the years/championships, will need to fix this somehow
    cTotalRaces = stats[0].find_all(class_="col")[1]
    cupWins = stats[0].find_all(class_="col")[2]
    cTopFives = stats[0].find_all(class_="col")[3]
    cTopTens = stats[0].find_all(class_="col")[4]
    cPoles = stats[0].find_all(class_="col")[5]
 

    '''
    driverFileAppend = {
        "driver": entry,
        "wins": cTotalRaces.text,
        "top5s": cTopFives.text,
        "top 10s": cTopTens.text
    }
    '''

    #should the data be proper numbers? hmmm
    data[eInt] = {"name": entry, "races": cTotalRaces.text, "wins": cupWins.text, "top5s": cTopFives.text, "top10s": cTopTens.text, "poles": cPoles.text, "yearStart": cYrFirst, "yearLast":  cYrLast, "Championships": str(champCount)}

    #print(data[eInt])

    eInt+=1


print(data)
with open('sample.json', 'w') as outfile:
    json.dump(list(data.values()), outfile, indent = 4)
    #y = json.dumps(driverFileAppend, indent=4, sort_keys=True)
    #print(y)
    #print(entry + ": " + grabDriverWins(entry))



