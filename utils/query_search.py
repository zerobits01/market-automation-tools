import json
import pprint
import urllib
import requests
# from googlesearch import search
from bs4 import BeautifulSoup
from utils.file_io import write_file
from utils.file_io import read_file_and_return_per_line


def send_request(link):
    return requests.get(link,
                                headers={"User-Agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0"\
                "Safari/537.36"}
    )


def gquery_return_response_text(query, img_mode=False):
    text = urllib.parse.quote_plus(query)
    if img_mode:
        url = 'https://google.com/search?q=' + text + "&tbm=isch"
    else:
        url = 'https://google.com/search?q=' + text
    return send_request(url).text


def search_query_in_google(keywords):
    # print(f"gonna search these {key_words}")
    first_three_ranks = []
    for query in keywords:
        resp_text = gquery_return_response_text(
            query=query
        )
        soup = BeautifulSoup(resp_text, 'html.parser')
        for link in soup.find_all(
            'a', attrs={"jscontroller": 'M9mgyc'}, href=True):
            if 'google' in link['href']:
                continue
            first_three_ranks.append(link['href'])
    # print(first_three_ranks)
    return first_three_ranks[0:3]


def get_google_images_seo_related(keywords):
    # how to search:
    # div with attribute jscontroller="ONqfcd" 
    # => if exist list inside that => get all "a span" and text of that span 
    results = dict(zip(keywords, list(len(keywords)*[[]])))
    for query in keywords:
        print(f"checking {query} on images")
        resp_text = gquery_return_response_text(
            query=query,
            img_mode=True
        )
        soup = BeautifulSoup(resp_text, 'html.parser')
        spans = soup.find_all(
            "div", attrs={"jscontroller": "ONqfcd"})[0].find_all(
                "span", class_="VlHyHc"
        )
        for span in spans:
            results[query].append(span.text)
    pprint.pprint(str(results))
    write_file(
        'google-image.txt',
        pprint.pformat(results)
        # json.dumps(results, indent=4, sort_keys=True)
    )


def get_seo_related_in_ranks(kw_path):
    keywords = read_file_and_return_per_line(
        kw_path
    )
    get_google_images_seo_related(keywords=keywords)
    first_ranks = search_query_in_google(keywords=keywords)
    extracted_data = {
        'alt_tags': [],
        'meta': [],
        'title': [],
        'h1': [],
        'h2': [],
        'images': []
    } # have to check mehdi
    for link in first_ranks:
        print(f"checking this {link}")
        response = send_request(link).text
        soup = BeautifulSoup(response, 'html.parser')        
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
        print(extracted_data['h1'], extracted_data['h2'])
    # print(json.dumps(extracted_data, indent=4, sort_keys=True))
    pprint.pprint(str(extracted_data))
    write_file(
        'in-site.txt',
        pprint.pformat(extracted_data)
    )
