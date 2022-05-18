from asyncio.windows_events import NULL
import requests
import sys
from bs4 import BeautifulSoup
import os
from github_utils import get_github_repo, upload_github_issue

book_title = []
book_isbn = []
book_writer = []

data = [
    book_title,
    book_isbn,
    book_writer
]

def page(index):
    return requests.get('https://book.naver.com/bookdb/book_detail.naver?bid=' + str(index))

def crawler(i): 
    #url = 'https://book.naver.com/bookdb/book_detail.naver?bid=15052904'
    #url = 'https://book.naver.com/bookdb/book_detail.naver?bid=21480555'
    response = page(i)
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

            if 'ISBN' in tag.text:
                isbn = tag.text.split('|')[1]
                isbn = isbn.replace('ISBN', '')
                isbn = isbn.strip()
    
    ### book_info add
    book_title.append(title)
    book_isbn.append(isbn)
    book_writer.append(writer)

def main(arg) :
    startNumber = int(arg)
    for i in range(startNumber, startNumber + 10):
        crawler(i)

    ### Check data
    '''
    for row in range(len(data[0])):
        d = []
        for col in range(len(data)):
            d.append(data[col][row])
        print(d)
    '''

def changeContens(list_data) :
    # list가 오게 됨
    # str로 파싱작업 해줌
    contents = ''
    for row in range(len(data[0])):
        str = ''
        str += data[0][row] + '|'
        str += data[1][row] + '|'
        str += data[2][row] + ' <br> \n'
        contents += str
        #print(str)

    return contents

def editTextFile(current_arg) :
    new_content = int(current_arg) + 10
    text_file_path = './start_number.txt'
    with open(text_file_path, 'w') as f:
        f.write(str(new_content))

if __name__ == '__main__':
    argument = sys.argv
    #argument.append(1)
    if len(argument) > 1:
        main(argument[1])

        access_token = os.environ['MY_GITHUB_TOKEN']
        repository_name = "isbn-crawling-with-python"

        issue_title = f"ISBN Crawling Data StartNumber : {argument[1]}"
        upload_contents = changeContens(data)
        repo = get_github_repo(access_token, repository_name)
        upload_github_issue(repo, issue_title, upload_contents)

        print('Upload Github Issue Success!')

        editTextFile(argument[1])

        print('Edit TextFile')
        