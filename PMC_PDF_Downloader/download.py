# API Name: OA(Open Access)
# Description: Download articles automately by inputing the author's name
# URL: https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi
# Author: Yifu Tian, CUHKSZ
# Date: 2024/3/22~2024/3/25

import requests
import xml.etree.ElementTree as ET
import os
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def search_articles_by_author(author_name):
    """Input the author's name and return a list of articles' PMC IDs."""
    search_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi'
    params = {
        'term': author_name + '[AUTH]',
        'tool': 'yifu',
        'email': '121090517@link.cuhk.edu.cn'
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()  # raise an error if the HTTP request returns a failed status code

    # parse the returned XML data
    root = ET.fromstring(response.content)
    pmc_ids = [record.attrib['id'] for record in root.findall('.//record')]

    return pmc_ids
def download_pmc_article(pmc_id, directory='downloaded_articles'):
    global cnt
    download_url = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/'

    """
    Sometimes the server will check certain values in the HTTP request header, such as User-Agent,
    to confirm whether the request comes from a browesr instead a script or automated tool.
    Add the User-Agent header here to simulate the browser's request.
    """
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    
    response = requests.get(download_url, headers=headers)
    response.raise_for_status()  


    file_name = os.path.join(directory, f'{pmc_id}.pdf')

    with open(file_name, 'wb') as file:
        file.write(response.content)

    print(f'Article {file_name} has been downloaded to {directory} successfully.')
    cnt += 1
author_name = input("Enter the author's name: \n")  # You may modify here for your convenience
directory = f'{author_name} articles'
create_dir(directory)

pmc_ids = search_articles_by_author(author_name)
cnt = 0
for pmcid in pmc_ids:
    download_pmc_article(pmcid, directory)
print(f"{len(pmc_ids)} requests, {cnt} succeeded, {len(pmc_ids)-cnt} failed.")

