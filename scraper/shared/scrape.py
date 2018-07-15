import requests

def scrape_reddit(subreddit_name):
    url = 'https://www.reddit.com/r/'+subreddit_name+'/.json'
    with requests.Session() as s:
        s = requests.Session()
        s.auth = ('ladzinski', 'screamforme')
        s.headers.update({'user-agent': 'Mozilla/5.0'})
        response = s.get(url,)
        datakey = {}
        for post in response.json()['data']['children']:
            key = post['data']['title']
            datakey.setdefault(key, [])
            datakey[key].append(post['data']['url'])
            datakey[key].append(post['data']['permalink'])
            datakey[key].append(post['data']['thumbnail'])
    return datakey

def scrape_gnews(region):
    url = ('https://newsapi.org/v2/top-headlines?'
           'country='+region+'&apiKey=9ce344d913ff4e8ca339cd99da25b1d6')
    response = requests.get(url)
    datakey = {}
    for post in response.json()['articles']:
        key = post['title']
        datakey.setdefault(key, [])
        datakey[key].append(post['url'])
        datakey[key].append(post['source']['name'])
        datakey[key].append(post['urlToImage'])
    return datakey

