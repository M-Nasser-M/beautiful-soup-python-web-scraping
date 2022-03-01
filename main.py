from bs4 import BeautifulSoup
import requests
import json

url = "https://news.ycombinator.com/"
output_json = []


def handle_page(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    titles = soup.select('.titlelink')
    votes = soup.select('.subtext')
    page_res = create_organized_list(titles, votes)
    return page_res


def sort_by_votes(organized_list):
    return sorted(organized_list, key=lambda k: k["points"], reverse=True)


def create_organized_list(titles_list, votes_list):
    organized_list = []
    for idx, item in enumerate(titles_list):
        point = int(votes_list[idx].select('.score')[0].text.replace(" points", "")) if votes_list[idx].select(
            '.score') else 0
        organized_list.append({'title': item.text, 'link': item.get('href'),
                               "points": point})
    return organized_list


for i in range(10):
    html = None
    if i == 0:
        html = requests.get(url)
    else:
        html = requests.get(f"{url}news?p={i + 2}")
    page_output = handle_page(html)
    output_json = [*output_json, *page_output]

output_json = sort_by_votes(output_json)

with open("output.json", 'w') as file_writer:
    json.dump(output_json, file_writer, indent=2)
