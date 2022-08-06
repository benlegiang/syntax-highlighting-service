from concurrent.futures import ThreadPoolExecutor, as_completed, thread
from logging import root
from threading import *
import time
from webbrowser import get
from bs4 import BeautifulSoup
import requests


github = 'https://github.com/'

python_trending_repos = 'https://github.com/trending/python?since=daily'
java_trending_repos = 'https://github.com/trending/java?since=daily'
kotlin_trending_repos = 'https://github.com/trending/kotlin?since=daily'

python_file_ex = '.py'
java_file_ex = '.java'
kotlin_file_ex = '.kt'

branches = ['/tree/master', '/tree/main', '/blob/master', '/blob/main']
invalid_dirs = ['/tree/master/.', '/tree/main/.']
scape_dir_depth = 4

results = []


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
                    if code_lang_extension in href:
                        code_file_urls.append(github + href)
                    else: 
                        directory_urls.append(github + href)
                else:
                    continue
        
        return directory_urls, code_file_urls
        
    except:
        return [], []

def get_code_file_urls_from_repo_url(code_lang_extension, root_url, iteration = 0, directory_urls = [], code_file_urls = []):

    # Termination condition 
    if iteration == scape_dir_depth:
        results.append(code_file_urls)
        return None

    # Start the search from the root directory of repo
    # Code files present in root dir are saved in 'c_urls'
    
    if iteration == 0:
        d_urls, c_urls = get_dirs_and_files_from_dir_url(code_lang_extension, root_url)
        code_file_urls.extend(c_urls)

        get_code_file_urls_from_repo_url(code_lang_extension, root_url, iteration + 1, d_urls, code_file_urls)
    else:
        sub_dir_urls_from_dir = []
        for dir in directory_urls:
            # print(dir)
            dir_urls, c_urls = get_dirs_and_files_from_dir_url(code_lang_extension, dir)
            sub_dir_urls_from_dir.extend(dir_urls)
            code_file_urls.extend(c_urls)
            # print(code_file_urls)

        get_code_file_urls_from_repo_url(code_lang_extension, root_url, iteration + 1, sub_dir_urls_from_dir, code_file_urls)


def get_source_code_from_file(html):

    pass

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


def run(code_lang):

    print("Start scraping...")

    t1_start = time.perf_counter()
    root_urls, code_lang_extension = get_root_urls(code_lang)
    
    threads = []

    test = [root_urls[0], root_urls[1]]


    for url in test:
        worker = Thread(target=get_code_file_urls_from_repo_url, args=(code_lang_extension, url))
        worker.start()
        threads.append(worker)
    
    for process in threads:
        process.join()

    t1_stop = time.perf_counter()

    test = results

    for i in test:
        print(i)
        print("Files in repo: ", len(i))

    seconds = t1_stop - t1_start
    print(f'Finished scraping in {seconds} seconds')

    print("number of repos: ", len(root_urls))



if __name__ == '__main__':
    # runner('PYTHON3')
    run('PYTHON3')




# def runner(code_lang):

#     root_urls, code_lang_extension = get_root_urls(code_lang)
#     threads = []

#     with ThreadPoolExecutor(max_workers=20) as executor:
#         for url in root_urls:
#             threads.append(executor.submit(get_code_file_urls_from_repo_url, code_lang_extension, url))
#             time.sleep(2)

#         # Uncomment above and comment this since it's only for testing purposes    
#         # one_repo = urls[2]
#         # TODO: Fix this so that multi threading works with recursive function

#         # threads.append(executor.submit(get_code_file_urls_from_repo_url, code_lang_extension, one_repo))

#         for request in as_completed(threads):
#             print("PRINTING RESULT OF EACH SCRAPED REPO: ", request.result())