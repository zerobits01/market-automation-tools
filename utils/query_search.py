import json
import pprint
import urllib
import requests
# from googlesearch import search
from bs4 import BeautifulSoup
from utils.file_io import write_file
from utils.file_io import read_file_and_return_per_line

def send_request_return_response_text(query):
    pass

def search_query_in_google(kw_path):
    lines = read_file_and_return_per_line(
        kw_path
    )
    print(f"gonna search these {lines}")
    first_three_ranks = []
    for text in lines:
        text = urllib.parse.quote_plus(text)
        url = 'https://google.com/search?q=' + text
        response = requests.get(url,
            headers={"User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0"\
                "Safari/537.36"}
        )
        # print(url, response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all(
            'a', attrs={"jscontroller": 'M9mgyc'}, href=True):
            if 'google' in link['href']:
                continue
            first_three_ranks.append(link['href'])
    # print(first_three_ranks)
    return first_three_ranks[0:3]


def get_google_images_seo_related(keywords):
    # how to search:
    # https://www.google.com/search?q={SOMETHING HERE}&tbm=isch
    # div with attribute jscontroller="ONqfcd" 
    # => if exist list inside that => get all "a span" and text of that span 
    # soup.find_all("div", attrs={"jscontroller": "ONqfcd"})[0].find_all("span", class_="VlHyHc")
    pass


def get_seo_related_in_ranks(kw_path):
    first_ranks = search_query_in_google(kw_path=kw_path)
    extracted_data = {
        'alt_tags': [],
        'meta': [],
        'title': [],
        'h1': [],
        'h2': []
    } # have to check mehdi
    for link in first_ranks:
        response = requests.get(link,
                                headers={"User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0"\
                "Safari/537.36"}
        )
        soup = BeautifulSoup(response.text, 'lxml')        
        # adding alt tags
        images = soup.find_all('img', alt=True)
        images = [f"{i['alt']}\n" for i in images]
        for image in images:
            if image.strip() != "":
                extracted_data['alt_tags'].append(image)

        # adding meta descriptions
        meta_descriptions = soup.find_all('meta')
        meta_descriptions = [
            f"{i}\n" for i in meta_descriptions
        ]
        if len(meta_descriptions) != 0:
            extracted_data['meta'] = \
                extracted_data['meta'] + meta_descriptions
                
        # adding titles
        title = soup.find_all('title')
        title = f"{title[0].text}\n"
        extracted_data['title'].append(title)
         
        # adding h1 and h2 texts
        h1s = soup.find_all('h1')
        h2s = soup.find_all('h2')
        h1s = [f"{i.text}\n" for i in h1s]
        h2s = [f"{i.text}\n" for i in h2s]
        extracted_data['h1'] = extracted_data['h1'] + h1s
        extracted_data['h2'] = extracted_data['h1'] + h2s
    # print(json.dumps(extracted_data, indent=4, sort_keys=True))
    # pprint.pprint(str(extracted_data))
    write_file(
        'output.txt',
        json.dumps(extracted_data, indent=4, sort_keys=True)
    )
