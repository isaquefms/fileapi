import requests


def post_fake_data():
    # servidor local
    url = 'http://localhost:8000/api/files/'
    
    # enviando o arquivo csv para a api
    response = requests.post(url, files={'file': open('testfiles/input.txt', 'rb')})
    print(response.text, response.status_code, response.elapsed.total_seconds())


def post_data():
    # servidor local
    url = 'http://localhost:8000/api/files/'
    
    # enviando o arquivo csv para a api
    response = requests.post(url, files={'file': open('testfiles/input.csv', 'rb')})
    print(response.text, response.status_code, response.elapsed.total_seconds())
    
    
if __name__ == '__main__':
    post_data()
    # post_fake_data()
    