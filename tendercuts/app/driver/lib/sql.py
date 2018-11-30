
import MySQLdb as mdb

import datetime
import time


def run_sql_file(filename, connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection
    '''
    start = time.time()

    files = open(filename, 'r')

    for file in files:
        # sql = s = " ".join(file.readlines())
        print "Start executing: " + filename + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + file

        cursor = connection.cursor()
        cursor.execute(file.split('\n')[0])
        connection.commit()

        end = time.time()
        print "Time elapsed to run the query:"
        print str((end - start) * 1000) + ' ms'


def main():
    # import pdb
    # pdb.set_trace()
    connection = mdb.connect('127.0.0.1', 'root', 'root', 'dbmaster')
    run_sql_file("/home/asarudheen/api/jenkins/sqlpy.sql", connection)
    connection.close()

if __name__ == "__main__":
    main()
