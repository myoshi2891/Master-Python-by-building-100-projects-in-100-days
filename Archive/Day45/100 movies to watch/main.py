import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Find all movie titles
all_movies = soup.find_all("h3", class_="title")

movie_titles = [movie.text.strip() for movie in all_movies]

# print(movie_titles[::-1])

# for n in range(len(movie_titles) - 1, 0, -1):
#     print(f"{movie_titles[n]}")

movies = movie_titles[::-1]

with open("movies.txt", "w") as file:
    for movie in movies:
        file.write(f"{movie}\n")
