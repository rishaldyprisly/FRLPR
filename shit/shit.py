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
        # Create a new record
        sql = "INSERT INTO `stock` (`nama`, `jenis`) VALUES (%s, %s)"
        cursor.execute(sql, ('H24', 'oil filter'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `nama`, `jenis` FROM `stock` WHERE `nama`=%s"
        cursor.execute(sql, ('gajah tunggal tire 24',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
