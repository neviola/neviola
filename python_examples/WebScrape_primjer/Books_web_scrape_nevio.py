'''
Spajanje na navedeni url, sprema se cijena i link za svaku knjigu u kategoriji "Mystery"
Nakon toga se nalazi najjeftinija i najskuplja knjiga te se ispisuju detalji za te knjige
Na kraju je moguce spremiti te informacije u .txt file
'''



from bs4 import BeautifulSoup
import requests

book_dict = {}     # {price: 'link'}


def find_books(page):
    '''
    Prolazi kroz svaku knjigu na stranici i sprema cijenu i link za svaku knjigu u book_dict
    '''

    url = f'https://books.toscrape.com/catalogue/category/books/mystery_3/page-{page}.html'
    html = requests.get(url)
    if html.ok == False:
        return -1

    soup = BeautifulSoup(html.text, 'html.parser')

    for book in soup.find_all('article', class_="product_pod"):
        book_link = book.h3.a['href']
        book_link = book_link.replace('../../../', '')

        # book_title = book.h3.a['title']               # uncomment za sve naslove knjiga
        # print(book_title)

        book_price = book.find('div', class_="product_price").p.text
        book_price = book_price.replace('Â£', '')

        book_dict[float(book_price)] = book_link        # problem ako neke knjige imaju identicne cijene?


def book_info(link):
    info_list = []
    html = requests.get(f'https://books.toscrape.com/catalogue/{link}').text
    soup = BeautifulSoup(html, 'html.parser')
    
    book_title = soup.find('div', class_="col-sm-6 product_main").h1.text
    book_price = soup.find('div', class_="col-sm-6 product_main").find('p', class_="price_color").text.replace('Â£','')
    book_descript = soup.find('article', class_="product_page").find('p', class_=None).text
    print(f'Title: {book_title}\nPrice: £{book_price}\nDescription: {book_descript}')

    info_list.append(f'Title: {book_title}')
    info_list.append(f'Price: £{book_price}')
    info_list.append(f'Description: {book_descript}')

    book_avail = soup.find_all('tr')[5].td.text
    print(f'Availability: {book_avail}')
    info_list.append(f'Availability: {book_avail}')

    book_review = soup.find_all('tr')[6].td.text
    print(f'Number of reviews: {book_review}')
    info_list.append(f'Number of reviews: {book_review}')

    return info_list


odg = None
page = 0
while odg != -1:
    page += 1                                                     # krece od 1. stranice
    odg = find_books(page)                                        # ako return -1, response = False, zaustavlja se

print('Number of scraped pages: ', page-1, '\n')                  # za provjeru do koje stranice je dosao

# pronalazi linkove za najvecu i najmanju cijenu u book_dict... relative path link, treba dodati za puni url, taj link se dodaje u fukciju
min_price_link = book_dict[min(book_dict)]
max_price_link = book_dict[max(book_dict)]
##
print('LEAST EXPENSIVE BOOK IN "MYSTERY"')
min_lista = book_info(min_price_link)
print()
print('MOST EXPENSIVE BOOK IN "MYSTERY"')
max_lista = book_info(max_price_link)

option = input('\n   Save to .txt file?  [y/n]\n   ')
if option == 'y':
    with open('Books.txt', 'w', encoding='utf-8') as f:
        for line in min_lista:
            f.write(f'{line}\n')
        f.write('\n')
        for line in max_lista:
            f.write(f'{line}\n')


