import requests
from bs4 import BeautifulSoup

if __name__ =="__main__":
    save_f = open('links', 'r')
    links = save_f.readlines()
    save_f.close()
    visited = links[:1750]
    url_contains = '/wiki/'
    not_scrape = '/wiki/Minecraft_'
    start_node = "https://minecraft.fandom.com/wiki/Item"
    prefix='https://minecraft.fandom.com'
    save_f = open('links', 'a')
    for i in links[1750:]:
        if i not in visited:
            try:
                response = requests.get(i)
                print(i)
                if response.status_code == 200:
                    # Parse the HTML content of the page using BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Find all the anchor (a) tags in the body of the HTML
                    urls = soup.find_all('a')
                    # Extract and print the href attribute from each anchor tag
                    for link in urls:
                        href = link.get('href')
                        if href:
                            if  href.startswith(url_contains) and not_scrape not in href and 'Edition' not in href:
                                if len(href.split(':')) > 0:
                                    href = href.split(':')[0]
                                if len(href.split('#')) > 0:
                                    href = href.split('#')[0]
                                if len(href.split('?')) > 0:
                                    href = href.split('?')[0]
                                href = prefix + href
                                if href not in links:
                                    links.append(href)
                                    print(str(len(links)), str(len(visited)))
                                    save_f.write(href + '\n')
                visited.append(i)
            except:
                print("can't get it " + i)
                links.remove(i)
                if i in visited:
                    visited.remove(i)

