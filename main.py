import requests

url = 'http://apis.data.go.kr/1721000/msitannouncementinfo/businessAnnouncMentList'
params ={'serviceKey' : '', 'pageNo' : '1', 'numOfRows' : '10', 'returnType' : 'xml' }

response = requests.get(url, params=params)
print(response.content)

