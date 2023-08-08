import time
import re
import requests
from bs4 import BeautifulSoup

def wikipedia_content(): # getting all text from a random Wikipedia page
    url = "https://en.wikipedia.org/wiki/Special:Random"
    response = requests.get(url)

    if response.status_code == 200:
        page = response.content
        soup = BeautifulSoup(page, 'html.parser')

        soup = soup.find('div', class_='mw-parser-output') # sorting out elements that contain text

        classes = (value
                   for element in soup.find_all(class_=True)
                   for value in element["class"])
        error_list = list()
        for el in classes:
            if el == "mw-redirect" or el == "new" or el == "extiv":
                continue
            try:
                soup.find(class_=el).extract()
            except AttributeError:
                error_list.append(el)
                continue
        text = soup.text.strip()

        if len(text) > 2000:
            return text
        else:
            return wikipedia_content()
    else:
        time.sleep(1)
        wikipedia_content()

def get_text():
    content = wikipedia_content()



    content = content.replace("(listen)", "") # formatting the text
    content = re.sub("\(.*[^\x00-\x7F].*?\)", "", content)
    content = re.sub("\n+", "", content)
    content = re.sub("\s+", " ", content)
    content = re.findall("[A-Z][^!?]*?[\.!?]\s", content)
    for i in range(len(content)):
        content[i] = content[i].strip()
    
    return content

