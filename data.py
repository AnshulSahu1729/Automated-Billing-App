import mysql.connector
import pickle

user=input("Enter Username : ")
passwrd=input("Enter Password : ")

mydb=mysql.connector.connect(host='localhost',user=user,password=passwrd)
cur=mydb.cursor()

cur.execute('drop database if exists barcodedata')

cur.execute('create database barcodedata')

mydb=mysql.connector.connect(host='localhost',user=user,password=passwrd,database='barcodedata')
cur=mydb.cursor()

l_user=[user,passwrd]
f=open('user.dat','wb')
pickle.dump(l_user,f)
f.close()


cur.execute('create table productdata1 (`Barcode ID` varchar(100) primary key,`Product Name` varchar(1000),`Price` decimal(14,2))')

insrt1='insert into productdata1(`Barcode ID`,`Product Name`,`Price`) values(%s,%s,%s)'
vals1=[
    ('8904006302880','Body Deodrant Secret Temp','199'),
    ('8904043926612','TATA Pink Salt','90'),
    ('8901288230603','VICCO Turmeric Cream','185'),
    ('8902519012760','Classmate Notebook 384pgs','170'),
    ('8901023005817','Ezee Liq Detergent','110'),
    ('8906001227069','Stamp Pad','35'),
    ('8906003340018','Asli Sarson Oil','70'),
    ('8906071454068','Custard Powder (Vanilla)','45'),
    ('8901088000345','Parachute Coconut oil','111'),
    ('8901030904486','Lifebuoy Hand Wash','99'),
    ('8901396350101','Dettol Antiseptic Liquid','40')
]
cur.executemany(insrt1,vals1)
mydb.commit()

print('DataBase added Successfully!!')
