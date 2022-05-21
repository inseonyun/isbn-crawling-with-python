from asyncio.windows_events import NULL
import requests
import sys
from bs4 import BeautifulSoup
import os
from github_utils import get_github_repo, upload_github_issue, close_github_issue

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
    for i in range(startNumber, startNumber + 100):
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
    for row in range(len(list_data[0])):
        str = ''
        str += list_data[0][row] + ' | '
        str += list_data[1][row] + ' | '
        str += list_data[2][row] + ' <br> \n'
        contents += str
        #print(str)

    return contents

def changeListToString(list_data) :
    # list가 오게 됨
    # 파싱하기 좋게 줄 구분은 \n, 책명 저자 isbn은 |로 구분함
    contents = ''
    for row in range(len(list_data[0])):
        str = ''
        str += list_data[0][row] + '|'
        str += list_data[1][row] + '|'
        str += list_data[2][row] + '\n'
        contents += str

    contents = contents.rstrip()

    return contents

def editTextFile(contents, text_file_path) :
    with open(text_file_path, 'w', encoding='UTF-8') as f:
        f.write(contents)

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

        close_github_issue(repo, issue_title)

        print(f'{issue_title} close Issue Success!')

        # edit start_number.txt
        editTextFile(str(int(argument[1]) + 100), './start_number.txt')
        print('Write start_number.txt')

        # write book_info.txt
        text_contets = changeListToString(data)
        editTextFile(text_contets, './book_info.txt')
        print('Write book_info.txt')
        