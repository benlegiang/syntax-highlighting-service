from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import List
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
scape_dir_depth = 5


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
        print(e)
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
        
    except Exception as e:
        print(e)
        return None

def get_code_file_urls_from_repo_url(code_lang_extension, repo_url, iteration = 0, directory_urls = [], code_file_urls = []):

    # Termination condition 1
    if iteration == scape_dir_depth:
        return code_file_urls

    # Termination condition 2
    if iteration > 0 and len(directory_urls) == 0:
        return code_file_urls

    # Start the search from the root directory of repo
    # Code files present in root dir are saved in 'c_urls'
    
    if iteration == 0:
        d_urls, c_urls = get_dirs_and_files_from_dir_url(code_lang_extension, repo_url)
        code_file_urls.extend(c_urls)
        iteration += 1

        get_code_file_urls_from_repo_url(code_lang_extension, repo_url, iteration, d_urls, code_file_urls)

    sub_dir_urls_from_dir = []
    for dir in directory_urls:
        # print(dir)
        dir_urls, c_urls = get_dirs_and_files_from_dir_url(code_lang_extension, dir)
        sub_dir_urls_from_dir.extend(dir_urls)
        code_file_urls.extend(c_urls)
        # print(code_file_urls)
    
    iteration += 1

    get_code_file_urls_from_repo_url(code_lang_extension, repo_url, iteration, sub_dir_urls_from_dir, code_file_urls)



def test(code_lang_extension, url):
    result = get_code_file_urls_from_repo_url(code_lang_extension, url)

    return result


def get_source_code_from_file(html):

    pass

def runner(code_lang):

    if code_lang == 'PYTHON3':
        repos = get_trending_repo_urls(python_trending_repos)
        code_lang_extension = python_file_ex
    elif code_lang == 'JAVA':
        repos = get_trending_repo_urls(java_trending_repos)
        code_lang_extension = java_file_ex
    elif code_lang == 'KOTLIN':
        repos = get_trending_repo_urls(kotlin_trending_repos)
        code_lang_extension = kotlin_file_ex

    urls = repos
    threads = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        # for url in urls:
        #     threads.append(executor.submit(get_code_file_urls_from_repo_url, code_lang_extension, url))
        #     time.sleep(3)

        # Uncomment above and comment this since it's only for testing purposes    
        one_repo = urls[0]
        # TODO: Fix this so that multi threading works with recursive function

        threads.append(executor.submit(test, code_lang_extension, one_repo))


        for request in as_completed(threads):
            print(request.result())
            pass

if __name__ == '__main__':
    runner('PYTHON3')
