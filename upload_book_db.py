import pymysql
import numpy as np
import sys

def db_connect(arg_host, arg_user, arg_pass, arg_db, data) :
    # set Value
    con_host = arg_host
    con_user = arg_user
    con_password = arg_pass
    con_db = arg_db

    # connect DB
    print('Connect DB')
    conn = pymysql.connect(host=con_host, user=con_user, password=con_password, db=con_db, charset='utf8')
    cursor = conn.cursor()

    db_insert(cursor, data)
    db_save(conn)

def db_insert(cursor, data) :
    print('insert Data')
    for row in range(len(data[0])):
        # 책 수량 0~10까지 난수 생성하여 넣음
        quantity = np.random.randint(0, 10)

        # insert Data
        # 테이블명 변경 필요
        sql = 'insert into book_status values(%s, %s, %s, %s)'
        vals = (data[0][row], data[1][row], data[2][row], quantity)
        cursor.execute(sql, vals)

def db_save(conn) :
    # save conn 
    print('Save DB')
    conn.commit()

    # Close DB
    print('Close DB')
    conn.close()

def readTextFile(text_file_path) :
    book_title = []
    book_isbn = []
    book_writer = []

    contents = [
        book_title,
        book_isbn,
        book_writer
    ]
    temp = ''
    with open(text_file_path, 'r', encoding='UTF-8') as f:
        temp = f.read()

    rows = temp.split('\n')

    for i in range(len(rows)) :
        data = rows[i].split('|')
        book_title.append(data[0])
        book_isbn.append(data[1])
        book_writer.append(data[2])

    return contents

if __name__ == '__main__':
    argument = sys.argv
    if len(argument) > 4:
        print('Process DB Start!!!!')
        file_data = readTextFile('./book_info.txt')
        db_connect(argument[1], argument[2], argument[3], argument[4], file_data)

        print('Process DB End!!!!')