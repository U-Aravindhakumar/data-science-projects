import requests
from bs4 import BeautifulSoup
url = "https://www.cricbuzz.com/live-cricket-scorecard/91814/aus-vs-ind-5th-test-india-tour-of-australia-2024-25"
data = requests.get(url)
print(data)

soup = BeautifulSoup(data.content, 'html.parser')
# print(soup.title.parent.name)
# print(soup.prettify())
# b = (soup.find (class_ = "row test-site"))
# a = b.find_all("p")
# print(a)
# for i in a:
#     print(i.text)

var = (soup.find(class_  = "ng-scope"))
print(var.find_all())