import requests

r = requests.get('https://get.geojs.io/')
print(r)
ip_requests = requests.get('https://get.geojs.io/v1/ip.json')
ipadd = ip_requests.json()['ip']
print(ipadd)

url = 'https://get.geojs.io/v1/ip/geo/' + ipadd + '.json'
geo_request = requests.get(url)
geo_data = geo_request.json()
#print(geo_data)
print(geo_data['latitude'])
print(geo_data['city'])
print(geo_data['region'])
print(geo_data['country'])