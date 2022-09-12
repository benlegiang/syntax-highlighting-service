import requests
from concurrent.futures import ThreadPoolExecutor
import json
import sys


annotation_api_url = 'http://localhost:8081/api/v1/highlight'

def send_single_entry(code_lang, src, index):

    res = requests.post(annotation_api_url, json={
        "codeLanguage": code_lang,
        "sourceCode": src
    })

    print(f'File {index} sent')
    return res.status_code
        
def annotate_files(code_lang, file_name):
    data = [json.loads(line) for line in open(file_name, 'r')]


    with ThreadPoolExecutor(max_workers=6) as executor:
        threads = []

        for i in range(len(data)):
            threads.append(executor.submit(send_single_entry, code_lang, data[i]['source'], i))

if __name__ == '__main__':
    annotate_files(sys.argv[1], sys.argv[2])
    
