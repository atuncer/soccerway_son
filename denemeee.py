import psycopg2 as psy
con = psy.connect(
    host = "db-bahispesinde1.cwln7t9ajzcz.eu-central-1.rds.amazonaws.com",
    database = "postgres",
    user = "Adminov",
    password = "amdin2323",
    port = "5435"
)


with con.cursor() as cur:
    # cur.execute("insert into tmp values('a','a','a','a','2021/12/29',1,1,'a','a','a')")
    # con.commit()
    cur.execute("Select distinct(hafta) from fikstur_premier where tarih < now() order by hafta asc")
    a = cur.fetchall()
    print(a)