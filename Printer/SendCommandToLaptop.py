import requests

#x = requests.get('http://192.168.1.41:5000/')
#x = requests.get('http://148.75.223.98:4000/')

url = 'http://192.168.1.41:5000/test'
dictToSend = {'red':'red','blue':'blue','green':'green'}
res = requests.post(url, data=dictToSend)