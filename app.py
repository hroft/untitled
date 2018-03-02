#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
import os
from mysql.connector import MySQLConnection, Error
regex = r"from [0.*-9]* to [0-9].*"

# Обновление данных в таблице
def update_cdr(path, recordingfile):
    # read database configuration
    db_config = {'password': 'Paralaxx', 'host': 'localhost', 'user': 'root', 'database': 'asteriskcdrdb'}
    # prepare query and data
    query = """UPDATE cdr SET path=%s WHERE recordingfile =%s """
    data = (path, recordingfile)

    try:
        conn = MySQLConnection(**db_config)

        # update book title
        cursor = conn.cursor()
        cursor.execute(query, data)
       # print (query)
        # accept the changes
        conn.commit()

    except Error as error:
        print(error)

    finally:
	cursor.close()
        conn.close()
#рашифровка записи
def translite(path):
    tpath = path[0:-3]+"txt"
    #print tpath
    os.system('asrclient-cli.py --silent ' + path + ' > ' + tpath)
    result2 = re.sub("^\n", "", (re.sub(regex, "", open(tpath).read(), 0)), 0)
    os.remove(tpath)
    return result2
#Запрос на выборку
def query_with_fetchall():
    try:
        db_config = {'password': 'Paralaxx', 'host': 'localhost', 'user': 'root'                                                                 $
	conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        #cursor.execute("SELECT recordingfile, calldate FROM cdr ")
        cursor.execute("SELECT recordingfile, calldate, translation FROM cdr where  billsec > 0 and recordingfile <> ''")
        #rows = cursor.fetchall()
        for recordingfile, calldate, translation in cursor:
            path = (pathwavfunct(recordingfile, calldate))
            #if (not (translation == "")): пройтись по всем записям
            if (translation == ""): # пройтись только по не распозанным записям
                update_cdr(str(path), str(recordingfile))
                #print(translite(path))
                trans = translite(path)
                update_translite(str(trans), str(recordingfile))
    except Error as e:
        print(e)

    finally:
	cursor.close()
        conn.close()

# полный путь к wav файлу
def pathwavfunct(recordingfile, calldate ):
    return "/var/spool/asterisk/monitor/"+re.sub("-", "/", str (calldate)[0:10],                                                                 $



regex = r"from [0.*-9]* to [0-9].*"
query_with_fetchall()


