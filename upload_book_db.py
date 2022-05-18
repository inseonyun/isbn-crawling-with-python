import pymysql
import numpy as np

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
        sql = 'insert into Book_Status_Info values(%s, %s, %s, %d)'
        vals = (data[0][row], data[1][row], data[2][row], quantity)
        cursor.execute(sql, vals)

def db_save(conn) :
    # save conn 
    print('Save DB')
    conn.commit()

    # Close DB
    print('Close DB')
    conn.close()
