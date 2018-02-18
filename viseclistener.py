import socket
import pymysql.cursors
s = socket.socket()         
 
s.bind(('192.168.1.208', 9000 ))
s.listen(0)              


client, addr = s.accept()
content = client.recv(1024)
a = (content.decode("utf-8"))

print('PLATE NUMBER = ',(a[328:336]))
print('LANE = ', (a[469:477]))
print('LOCAL TIME = ',(a[589:615]))

connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='',
                                 db='lpr',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
        # Create a new record
    sql = 'INSERT INTO viseclpr (plate, lane, time) VALUES (%s, %s, %s)'
    cursor.execute(sql, (a[328:336], a[469:477], a[589:615]))

    connection.commit()
