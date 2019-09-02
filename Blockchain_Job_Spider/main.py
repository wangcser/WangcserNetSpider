import requests

list_url = "https://www.zhipin.com/c100010000/?query=%E5%8C%BA%E5%9D%97%E9%93%BE&page=1&ka=page-1"
job_url = "https://www.zhipin.com/job_detail/1913e38066dd3c8e1Hd40t--FVE~.html"
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "76be7673-acda-4945-8b2c-5fd3c1a591bb",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
querystring = {"ka": "search_list_1"}

r = requests.request("GET", list_url, headers=headers, params=querystring)
content = r.content.decode('utf-8')
# print(content.decode('utf-8'))

file = './zhipin/list_sample.html'
with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
