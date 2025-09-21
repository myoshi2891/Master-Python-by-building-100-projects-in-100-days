import requests
from bs4 import BeautifulSoup

# import lxml

response = requests.get("https://news.ycombinator.com/news")

soup = BeautifulSoup(response.text, "html.parser")
all_article_tags = soup.find_all(name="span", class_="titleline")
article_texts = []
article_links = []
for article_tag in all_article_tags:
    text = article_tag.getText()
    article_texts.append(text)
    link = article_tag.find("a").get("href")
    article_links.append(link)

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

largest_upvote_index = article_upvotes.index(max(article_upvotes))
print(f"The article with the most upvotes has {article_upvotes[largest_upvote_index]} upvotes. The article is titled '{article_texts[largest_upvote_index]}' and can be found at: {article_links[largest_upvote_index]}")

# print(article_texts)
# print(article_links)
# print(article_upvotes)
# with open("website.html") as file:
#     contents = file.read()

# soup = BeautifulSoup(contents, "html.parser")
# # print(soup.prettify())
# # print(soup.p)

# all_anchor_tags = soup.find_all(name="a")

# # for anchor_tag in all_anchor_tags:
#     # print(anchor_tag["href"])
#     # print(anchor_tag.getText())

# heading = soup.find(name="h1", id="name")
# # print(heading)

# section_heading = soup.find(name="h3", class_="heading")
# # print(section_heading.getText() if section_heading else "No section heading found")

# name = company_url = soup.select_one(selector="#name")
# # print(name)

# headings = soup.select(selector=".heading")
# print(headings)
