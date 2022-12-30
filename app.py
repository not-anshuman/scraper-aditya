import os
import requests
from bs4 import BeautifulSoup

# Set the search query and filetype
query = 'your search query'
filetype = 'pdf'
no_of_pages=5
# Set the Google search URL
for page in range(0, 10*no_of_pages, 10):
    url = f'https://www.google.com/search?q={query}+filetype:{filetype}&start={page}'

    # Make the request and get the search results page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the links on the page
    links = soup.find_all('a')

    # Iterate over the links and download each PDF
    for link in links:
        href = link.get('href')
        if href and '/url?q=' in href:
            # Extract the title from the link text
            title = link.text.strip()

            # Extract the real link from the Google redirect link
            real_link = href.split('&')[0][7:]

            # Download the PDF and save it to the current working directory
            if(real_link.endswith('.pdf') or ".pdf" in real_link):
                try:
                    pdf = requests.get(real_link)
                    with open(f'{title}.pdf', 'wb') as f:
                        f.write(pdf.content)
                    pdf = requests.get(real_link)
                    if pdf.headers["Content-Type"] == "application/pdf":
                        print(real_link)
                        with open(f'{title}.pdf', 'wb') as f:
                            f.write(pdf.content)
                            
                except requests.exceptions.RequestException:
                    continue


print('Finished downloading PDFs')