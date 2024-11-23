import requests
from bs4 import BeautifulSoup
from io import BytesIO

def scrap_a_movie(movie_url):
    movie_name = ""
    movie_genre = []
    movie_poster = ""

    # IMDb URL
    url = movie_url  # Replace with the IMDb page URL

    # Headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # Fetch the page with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error if the request fails

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the image element by class
        image_element = soup.find("img", class_="ipc-image")
        if image_element:
            # Extract image URL
            image_url = image_element.get("src")
            if image_url:
                print(f"Image URL: {image_url}")

                # Download the image
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                movie_poster = BytesIO(image_response.content)
            else:
                print("Image URL not found.")
        else:
            print("Image element not found.")

        name_element = soup.find('span', class_ = 'hero__primary-text')
        if name_element:
            movie_name = name_element.text
        else:
            print("Name not found")

        genre_elements = soup.find_all('span', class_='ipc-chip__text')
        movie_genre = [genre.text for genre in genre_elements]
        movie_genre.pop()



    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return movie_name, movie_genre, movie_poster
