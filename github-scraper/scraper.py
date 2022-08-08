from threading import *
import time
from bs4 import BeautifulSoup
import requests
import sys

github = 'https://github.com/'

python_trending_repos = 'https://github.com/trending/python?since=daily'
java_trending_repos = 'https://github.com/trending/java?since=daily'
kotlin_trending_repos = 'https://github.com/trending/kotlin?since=daily'

annotation_api_url_local = 'http://localhost:8081/api/v1/highlight'
annotation_api_url = 'http://syntax-highlighting-service-rest-api:8081/api/v1/highlight'

python_file_ex = '.py'
java_file_ex = '.java'
kotlin_file_ex = '.kt'

branches = ['/tree/master', '/tree/main', '/blob/master', '/blob/main']
invalid_dirs = ['/tree/master/.', '/tree/main/.']
scape_dir_depth = 4

scraped_file_urls = []
source_codes = []


def get_trending_repo_urls(language_trending_repo):
    try:
        html = requests.get(language_trending_repo).text
        soup = BeautifulSoup(html, features='html.parser')

        # Finds all repositories from the trending page
        repos = soup.find_all('h1', class_ = 'h3 lh-condensed')

        trending_repos_urls = []

        # Retrieves url from all trending repos
        for repo in repos:
            repo_link_tag = repo.find_all('a')
            for link in repo_link_tag:
                href = link.get('href')
                trending_repos_urls.append(github + href)

        return trending_repos_urls
    except Exception as e:
        return None

def get_dirs_and_files_from_dir_url(code_lang_extension, dir_url):
    try:
        single_repo_html = requests.get(dir_url, stream=True).text
        soup = BeautifulSoup(single_repo_html, features='html.parser')
        directories = soup.find_all('div', class_ = 'Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item')

        directory_urls = []
        code_file_urls = []

        for dir in directories:
            dir_link_tag = dir.find_all('a', class_ = 'js-navigation-open Link--primary')
            for link in dir_link_tag:
                href = link.get('href')
                is_href_in_branch = bool([el for el in branches if href != None and el in href])
                is_href_valid_dir = bool([el for el in invalid_dirs if href != None and el not in href])

                if is_href_in_branch == True and is_href_valid_dir == True:   
                    # if code_lang_extension in href:
                    if href.endswith(code_lang_extension):
                        code_file_urls.append(github + href)
                    else: 
                        directory_urls.append(github + href)
                else:
                    continue
        
        return directory_urls, code_file_urls
        
    except:
        return [], []

def get_code_file_urls_from_repo_url(code_lang_extension, root_url, iteration=0, directory_urls=[], code_file_urls=[]):

    # Termination condition 
    if iteration == scape_dir_depth:
        scraped_file_urls.append(code_file_urls)
        return None
    
    if iteration == 0:
        d_urls, c_urls = get_dirs_and_files_from_dir_url(code_lang_extension, root_url)
        code_file_urls.extend(c_urls)

        get_code_file_urls_from_repo_url(code_lang_extension, root_url, iteration + 1, d_urls, code_file_urls)
    else:
        sub_dir_urls_from_dir = []
        # code_file_urls_found = []
        for dir in directory_urls:
            dir_urls, c_urls = get_dirs_and_files_from_dir_url(code_lang_extension, dir)
            sub_dir_urls_from_dir.extend(dir_urls)
            code_file_urls.extend(c_urls)

        get_code_file_urls_from_repo_url(code_lang_extension, root_url, iteration + 1, sub_dir_urls_from_dir, code_file_urls)
    time.sleep(1)

def get_root_urls(code_lang):

    if code_lang == 'PYTHON3':
        repos = get_trending_repo_urls(python_trending_repos)
        code_lang_extension = python_file_ex
    elif code_lang == 'JAVA':
        repos = get_trending_repo_urls(java_trending_repos)
        code_lang_extension = java_file_ex
    elif code_lang == 'KOTLIN':
        repos = get_trending_repo_urls(kotlin_trending_repos)
        code_lang_extension = kotlin_file_ex

    return repos, code_lang_extension


def scrape(code_lang, repo_limit):

    print("Start scraping...")

    t1_start = time.perf_counter()
    root_urls, code_lang_extension = get_root_urls(code_lang)
    
    threads = []

    repo_root_urls = root_urls[0:repo_limit]
    

    for url in repo_root_urls:
        process = Thread(target=get_code_file_urls_from_repo_url, args=(code_lang_extension, 
        url, 0, [], []))
        process.start()
        threads.append(process)
    
    for process in threads:
        process.join()

    t1_stop = time.perf_counter()

    seconds = t1_stop - t1_start
    print(f'Finished scraping in {seconds} seconds')
    print(f'{len(repo_root_urls)} repositories scanned')

def extract_source_code_from_file(code_lang, num_tokens, extract_backwards):

    timeout = 10
    print(f'Waiting {timeout} seconds to avoid abuse timeout')
    time.sleep(timeout)
    temp_source_codes = []
    for repo in scraped_file_urls:
        for file in repo:
            time.sleep(0.5)
            single_file_html = requests.get(file, stream=True).text
            soup = BeautifulSoup(single_file_html, features='html.parser')
            lines = soup.find_all('td', class_="blob-code blob-code-inner js-file-line")

            if len(lines) > 0:
                src = ''
                for line in lines:
                    if line.text != '' or line.text != ' ':
                        src += line.text
                    else: continue
                # for line in lines:
                #     if filter_src_line(line, code_lang):
                #         l = line.text.replace('\n', ' ')
                #         src += line.text
                #     else:
                #         continue
                temp_source_codes.append(src)
            else: continue

    source_codes.extend(get_src_by_num_of_tokens(temp_source_codes, num_tokens, extract_backwards))
    
    print(f'{len(source_codes)} files found')

def filter_src_line(line, code_lang):

    if code_lang == 'PYTHON3':
        # if "#" in line or "'''" in line:
        if "#" in line:
            return False
        else:
            return True

    # Check other languages for comments

def get_src_by_num_of_tokens(temp_src, num_tokens, backwards):

    result = []
    for content in temp_src:
        content_space_separated = content.split()
        num_token_seq = len(content_space_separated)
        # Consider only whole tokens when slicing
        if num_tokens >= num_token_seq:
            result.append(content)
        
        if num_tokens < num_token_seq and not backwards:
            file_content = ''
            for token in content_space_separated[0:num_tokens]:
                file_content += token + ' '
            result.append(file_content)
        else:
            file_content = ''
            for token in content_space_separated[-num_tokens:]:
                file_content += token + ' '
            result.append(file_content)

    return result

def send_code_for_annotation(code_lang):
    print("Sending source codes to Annotation API...")

    batch_length = len(source_codes)
    try:
        for i in range(batch_length):
            res = requests.post(annotation_api_url, json={
                "codeLanguage": code_lang,
                "sourceCode": source_codes[i]
                })
            print(f"Sending file {i + 1}/{batch_length} with status code: {res.status_code}")

        print("Annotated files successfully!")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    scrape(sys.argv[1], int(sys.argv[2]))
    extract_source_code_from_file(sys.argv[1], int(sys.argv[3]), bool(sys.argv[4]))
    send_code_for_annotation(sys.argv[1])
