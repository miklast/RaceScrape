import requests
from bs4 import BeautifulSoup
import json
import time

def changeDriverPage(driver):
    page = requests.get(URL + "driver/" + driver.replace(" ", "_"))

#Set url to var to make it easier to call as needed
URL = "https://www.racing-reference.info/"
#placeholder driver for testing
extension = "driver/A_J_Allmendinger/"
page = requests.get(URL + extension)

#soup object
soup = BeautifulSoup(page.content, "html.parser")

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


