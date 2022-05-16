import requests
from bs4 import BeautifulSoup

book_title = []
book_isbn = []
book_writer = []

data = {
    'title':book_title,
    'isbn':book_isbn,
    'writer':book_writer
}

def page(index):
    html = requests.get('https://book.naver.com/bookdb/book_detail.naver?bid=')

def crawler(): 
    #url = 'https://book.naver.com/bookdb/book_detail.naver?bid=15052904'
    #url = 'https://book.naver.com/bookdb/book_detail.naver?bid=21480555'
    url = 'https://book.naver.com/bookdb/book_detail.naver?bid=2234942'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    ### 책 이름 정보 가져옴
    h2_tag = soup.findAll('h2')
    title = ''
    for tag in h2_tag:
        title = str(tag.text)

    ### 책 저자, ISBN 정보 가져옴
    writer = ''
    isbn = ''
    div_tag = soup.find('div', {'class':'book_info_inner'})
    for tag in div_tag:
        if '|' in tag.text:
            if '저자' in tag.text:
                writer = tag.text.split('|')[0]
                writer = writer.split(' ')[1]

            if 'ISBN' in tag.text:
                isbn = tag.text.split('|')[1]
                isbn = isbn.replace('ISBN', '')
                isbn = isbn.strip()
    
    ### book_info add
    book_title.append(title)
    book_isbn.append(isbn)
    book_writer.append(writer)

    ### Check data
    for row in data:
        for d in data[row]:
            print(d)

crawler()