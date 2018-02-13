import glob
import os
import pymysql.cursors
import time


#while total > 1: 
files = os.listdir('D:\camp\htdocs\LPR')
list_of_files = glob.glob('D:\camp\htdocs\LPR\*.lpr') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='',
                                 db='lpr',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

while True:
    
     with open(latest_file,'rb') as f:
         f = f.readlines()
         print ('')
         print('PLATE NUMBER = ',(f[5]))
         print ('LOCATION = ', (f[10]))
         print ('LOCAL TIME = ',(f[15]))
     with connection.cursor() as cursor:
        # Create a new record
         sql = 'INSERT INTO viseclpr (plate, lane, time) VALUES (%s, %s, %s)'
         cursor.execute(sql, (f[5], f[10], f[15]))
         connection.commit()
         connection.close()
         for latest_file in list_of_files:
             os.unlink(latest_file)
             time.sleep(0.5)
             
         
