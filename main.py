import requests
from bs4 import BeautifulSoup

#Set url to var to make it easier to call as needed
URL = "https://www.racing-reference.info/"
#placeholder driver for testing
extension = "driver/A_J_Allmendinger/"
page = requests.get(URL + extension)

#soup object
soup = BeautifulSoup(page.content, "html.parser")


driverName = soup.find(class_="dataCont")
seriesResults = soup.find_all(class_="seriesHeader")

print(driverName.find("h1").text.strip())
print("")

#finds series name and prints
for sResult in seriesResults:
    seriesElement = sResult.find("h1")
    print(seriesElement.text.strip())

#print(seriesResults)