#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
import os
import configparser
import pymysql.cursors

#собираем данные для работы из script.conf файла
conf = configparser.RawConfigParser()
conf.read('script.conf')
host = conf.get('db_autch', 'host')
user = conf.get('db_autch', 'user')
password = conf.get('db_autch', 'password')
db_name = conf.get('db_autch', 'db_name')
regex = r"from [0.*-9]* to [0-9].*"

def update_cdr(connection, path, recordingfile):
    #
    # # Connect to the database
    # connection = pymysql.connect(host= host,
    #                              user=user,
    #                              password= password,
    #                              db=db_name,
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = '''UPDATE cdr SET path=%s WHERE recordingfile =%s'''
            cursor.execute(sql, (path, recordingfile))
    finally:
        connection.close()

    # запись расшифровки в БД
    # Обновление данных в таблице
def update_translite(connection, trans, recordingfile):
    # connection = pymysql.connect(host= host,
    #                              user=user,
    #                              password= password,
    #                              db=db_name,
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)
    #                            cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = '''UPDATE cdr SET translation=%s WHERE recordingfile =%s '''
            cursor.execute(sql, (trans, recordingfile))
    finally:
        connection.close()

#рашифровка записи
def translite(path):
    tpath = path[0:-3]+"txt"
    #print tpath
    os.system('asrclient-cli.py --silent ' + path + ' > ' + tpath)
    # result2 = re.sub("^\n", "", (re.sub(regex, "", open(tpath).read(), 0)), 0)
    # os.remove(tpath)
    return result2


#запрос на выборку
def query_fetchall(connection):
    # # Connect to the database
    # connection = pymysql.connect(host= host,
    #                              user=user,
    #                              password= password,
    #                              db=db_name,
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT recordingfile, calldate, translation FROM cdr where  billsec > 0 and recordingfile <> ''"
            cursor.execute(sql)
            for recordingfile, calldate, translation in cursor:
                path = (pathwavfunct(recordingfile, calldate))
                # if (not (translation == "")): пройтись по всем записям
                if (translation == ""):  # пройтись только по не распозанным записям
                    update_cdr(str(path), str(recordingfile))
                    # print(translite(path))
                    trans = translite(path)
                    update_translite(str(trans), str(recordingfile))
    finally:
        connection.close()

# полный путь к wav файлу
def pathwavfunct(recordingfile, calldate ):
    return "/var/spool/asterisk/monitor/" + re.sub("-", "/", str(calldate)[0:10], 0) + "/" + recordingfile

def tester(connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT recordingfile, calldate FROM cdr where  billsec > 0 and recordingfile <> '' and translation = ''"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(row['calldate'])
                print(row['recordingfile'])
                # recordingfile = row[0]
                # calldate = row[1]
                path = (pathwavfunct(row['recordingfile'], row['calldate']))
                # if (not (translation == "")): пройтись по всем записям
                trans = translite(path)
                # print(trans)
                # print(path)
                # # print(result)
                # print(recordingfile)
                # update_translite(str(trans), str(recordingfile))
    finally:
        connection.close()

def main():
    connection = pymysql.connect(host= host,
                                 user=user,
                                 password= password,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    tester(connection)




if __name__ == '__main__':
    main()

    # query_fetchall(connection)

