# HTTP Client (ThreadPool)
import requests
from concurrent.futures import ThreadPoolExecutor

def make_request(url):
    response = requests.get(url)
    return response.json()

def main():
    urls = [
        'http://localhost:8081/',
        'http://localhost:8081/path1',
        'http://localhost:8081/path2'
    ]
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(make_request, urls)
        for result in results:
            print("Response:", result)

if __name__ == '__main__':
    main()