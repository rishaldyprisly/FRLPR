import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='',
                             db='aidb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `nama`, `jenis` FROM `stock` WHERE `nama`=%s"
        cursor.execute(sql, ('gajah tunggal tire 24',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
