import requests
from bs4 import BeautifulSoup


book_title = []
book_isbn = []
book_writer = []

data = [
    book_title,
    book_isbn,
    book_writer
]

def crawler(): 
    response = requests.get('https://book.naver.com/bookdb/book_detail.naver?bid=1')
    soup = BeautifulSoup(response.content, "html.parser")

    ### 책 이름 정보 가져옴
    h2_tag = soup.findAll('h2')
    title = ''
    for tag in h2_tag:
        title = str(tag.text).replace('\xa0', ' ')

    ### 책 저자, ISBN 정보 가져옴
    writer = ''
    isbn = ''
    div_tag = soup.find('div', {'class':'book_info_inner'})
    for tag in div_tag:
        if '|' in tag.text:
            if '저자' in tag.text:
                writer = tag.text.split('|')[0]
                writer = writer.split('저자 ')[1]
                writer = writer.replace('\xa0', ' ')

        if 'ISBN ' in tag.text:
            if '|' in tag.text:
                isbn = tag.text.split('|')[1]
                isbn = isbn.replace('ISBN', '')
            else :
                isbn = tag.text.split('ISBN')[1]
            isbn = isbn.strip()
    
    ### book_info add
    book_title.append(title)
    book_isbn.append(isbn)
    book_writer.append(writer)

crawler()