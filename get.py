import glob
import os
import pymysql.cursors


def files():
     os.listdir('D:\camp\htdocs\LPR')
     list_of_files = glob.glob('D:\camp\htdocs\LPR\*.lpr')
     latest_file = max(list_of_files, key=os.path.getctime)

     with open(latest_file,'rb') as f:
         f = f.readlines()
         print ('')
         print('PLATE NUMBER = ',(f[5]))
         print ('LOCATION = ', (f[10]))
         print ('LOCAL TIME = ',(f[15]))

def send():
	files()
     connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='',
                             db='lpr',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

     try:
         with connection.cursor() as cursor:
        # Create a new record
             sql = 'INSERT INTO viseclpr (plate, lane, time) VALUES (%s, %s, %s)'
             cursor.execute(sql, (f[5], f[10], f[15]))

         connection.commit()
         os.remove(latest_file)

     finally:
	     #os.remove(latest_file)
	     connection.close()
    #os.close(latest_file)

   
while True:
	files()
	send()
