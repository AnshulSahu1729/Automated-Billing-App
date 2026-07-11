import cv2
import customtkinter
from pyzbar.pyzbar import decode
from PIL import ImageTk, Image,ImageDraw,ImageFont
import pywhatkit
import mysql.connector
from decimal import Decimal
import pickle
import threading

f=open("user.dat",'rb')
l_user=pickle.load(f)

mydb=mysql.connector.connect(host='localhost',user=l_user[0],password=l_user[1],database='barcodedata')
cur=mydb.cursor()

root=customtkinter.CTk()
# root.geometry("1280x720")
root.after(0, lambda: root.state('zoomed'))
root.title('Automated Billing App')
cap=cv2.VideoCapture(0)


all_barcodes=[]
cur.execute('select `Barcode ID` from productdata1')
allbarcodes1=cur.fetchall()
for barcodetup1 in allbarcodes1:
    all_barcodes.append(barcodetup1[0])

used_barcodes=[]

title_frame=customtkinter.CTkFrame(root)
title_frame.pack()
customtkinter.CTkLabel(title_frame,text="Automated Billing App",font=("Arial Rounded MT Bold",28)).pack(pady=10)

root_body=customtkinter.CTkFrame(root)
root_body.pack(fill="both")
root_body.columnconfigure(0,weight=8)
root_body.columnconfigure(1,weight=2)
# root.rowconfigure(0,weight=1)
frame_left=customtkinter.CTkFrame(root_body,border_width=3)
frame_left.grid(row=0,column=0,sticky="nsew",padx=10,pady=20)
frame_right=customtkinter.CTkFrame(root_body,border_width=3)
frame_right.grid(row=0,column=1,sticky="nsew",padx=10,pady=20)

frame_phone=customtkinter.CTkFrame(frame_right)
frame_phone.pack(side='top',anchor='e',padx=30,pady=20)
customtkinter.CTkLabel(frame_phone,text='📞 : ',font=('Arial',20)).grid(row=0,column=0,padx=5,pady=5)
phone_entry=customtkinter.CTkEntry(frame_phone)
phone_entry.grid(row=0,column=1,padx=5,pady=5)
frame_cam=customtkinter.CTkFrame(frame_right)
frame_cam.pack(side="top")
label_cam=customtkinter.CTkLabel(frame_cam)
label_cam.grid(column=1,row=1,padx=20,pady=20)
label_txt=customtkinter.CTkLabel(frame_cam,text="Barcode",font=("Arial",25))
label_txt.grid(column=2,row=1,padx=20)


frame_data=customtkinter.CTkFrame(frame_left)
frame_data.pack(side='top',fill="x",padx=5,pady=10)
frame_data.columnconfigure(1,weight=1)
frame_data.columnconfigure(2,weight=8)
frame_data.columnconfigure(3,weight=1)
frame_data.columnconfigure(4,weight=2)
frame_data.columnconfigure(5,weight=1)
frame_data.columnconfigure(6,weight=4)
customtkinter.CTkLabel(frame_data,text='S. No').grid(row=0,column=1,padx=10,pady=10,sticky='ew')
customtkinter.CTkLabel(frame_data, text='Product Name').grid(row=0,column=2,padx=10,pady=10,sticky='ew')
customtkinter.CTkLabel(frame_data, text='Qty').grid(row=0,column=4,padx=10,pady=10,sticky='ew')
customtkinter.CTkLabel(frame_data, text='Price').grid(row=0,column=6,padx=10,pady=10,sticky='ew')

def send_whatsapp():
    phone="+91"+phone_entry.get()
    pywhatkit.sendwhats_image(phone,'invoice.png','',30,True,3)


def print_bill():
    len_data=len(data)

    img=Image.new('RGB',(800,1000),'white')
    draw=ImageDraw.Draw(img)

    font_title=ImageFont.truetype('C:/Windows/Fonts/ARLRDBD.ttf',36)
    font_content=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    font_total=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26)


    draw.text((400,100),'INVOICE',anchor='mm',fill='black',font=font_title)
    draw.line((50,200,50,(len_data*100+400)),fill='black',width=2)
    draw.line((130,200,130,(len_data*100+400)),fill='black',width=2)
    draw.line((500,200,500,(len_data*100+400)),fill='black',width=2)
    draw.line((580,200,580,(len_data*100+400)),fill='black',width=2)
    draw.line((750,200,750,(len_data*100+400)),fill='black',width=2)
    draw.line((50,200,750,200),fill='black',width=2)
    draw.line((50,280,750,280),fill='black',width=2)
    draw.line((50,(len_data*100+400),750,(len_data*100+400)),fill='black',width=2)
    draw.text((60,220),'S. No.',fill='black',font=font_content)
    draw.text((200,220),'Item Name',fill='black',font=font_content)
    draw.text((520,220),'Qty',fill='black',font=font_content)
    draw.text((620,220),'Price',fill='black',font=font_content)

    total=0
    i=0
    for items in data:
        draw.text((70,(300+i*100)),str(items[0]),fill='black',font=font_content)
        draw.text((150,(300+i*100)),str(items[1]),fill='black',font=font_content)
        draw.text((530,(300+i*100)),str(items[2]),fill='black',font=font_content)
        draw.text((600,(300+i*100)),'Rs. '+str(items[3]),fill='black',font=font_content)
        i+=1
        total+=items[3]

    draw.line((50,(300+len_data*100),750,(300+len_data*100)),fill='black',width=2)
    draw.text((400,(340+len_data*100)),'Total',fill='black',font=font_total)
    draw.text((600,(340+len_data*100)),'Rs. '+str(total),fill='black',font=font_total)

    img.save('invoice.png')
    
    threading.Thread(
        target=send_whatsapp,
        daemon=True
    ).start()


print_bill_button=customtkinter.CTkFrame(frame_right)
print_bill_button.pack(side='bottom',pady=50)
customtkinter.CTkButton(print_bill_button,width=100,height=50,text='E-Print',command=print_bill,font=('arial',18)).grid(row=0,column=0)

frame_total=customtkinter.CTkFrame(frame_right)
frame_total.pack(side='bottom',pady=20)
customtkinter.CTkLabel(frame_total,text='Total:',font=("Arial",25)).grid(row=0,column=0,pady=5,padx=10)

barcode=''
sum=0
sno=1

product_data=['','','','']
data=[]
qty_ref_list=[]


def update_cam():
    global sno
    global sum
    global barcode
    success,frame=cap.read()

    def addqty(a):
        global sum
        current_qty=qty_ref_list[a-1][0].cget('text')
        current_price_text=qty_ref_list[a-1][1].cget('text')
        current_price=current_price_text.split()
        current_price=current_price[1]
        actual_price=float(current_price)/float(current_qty)
        qty_ref_list[a-1][0].configure(text=str(int(current_qty)+1))
        qty_ref_list[a-1][1].configure(text='Rs. '+str(float(current_price)+float(actual_price)))
        sum+=Decimal(actual_price)
        customtkinter.CTkLabel(frame_total,text=str(sum)).grid(row=0,column=1)
        data[a-1][2]=int(current_qty)+1
        data[a-1][3]=float(current_price)+float(actual_price)


    def removeqty(a):
        global sum
        current_qty=qty_ref_list[a-1][0].cget('text')
        current_price_text=qty_ref_list[a-1][1].cget('text')
        current_price=current_price_text.split()
        current_price=current_price[1]
        actual_price=float(current_price)/float(current_qty)
        if int(current_qty)>=0:
            qty_ref_list[a-1][0].configure(text=str(int(current_qty)-1))
            qty_ref_list[a-1][1].configure(text='Rs. '+str(float(current_price)-float(actual_price)))
        sum-=Decimal(actual_price)
        customtkinter.CTkLabel(frame_total,text=str(sum)).grid(row=0,column=1)
        data[a-1][2]=int(current_qty)-1
        data[a-1][3]=float(current_price)-float(actual_price)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w = frame_rgb.shape[:2]
    s = min(h, w)
    cropped = frame_rgb[(h - s) // 2:(h + s) // 2, (w - s) // 2:(w + s) // 2]
    img = customtkinter.CTkImage(Image.fromarray(cropped), size=(220, 220))
    label_cam.configure(image=img, text="")
    label_cam.image = img

    if decode(frame)!=[]:
        # print(decode(frame))
        for code in decode(frame):
            barcode = code.data.decode("utf-8")
            label_txt.configure(text=f'{code.type} \n {barcode}')

            if (barcode in all_barcodes) and (barcode not in used_barcodes):
                all_barcodes.remove(barcode)
                used_barcodes.append(barcode)
                cur.execute(f'select `Product Name` from productdata1 where `Barcode ID`={barcode}')
                productname=cur.fetchone()
                productname=productname[0]
                cur.execute(f'select `Price` from productdata1 where `Barcode ID`={barcode}')
                price = cur.fetchone()
                price=price[0]
                customtkinter.CTkLabel(frame_data,text=str(sno)).grid(row=sno,column=1,padx=10,pady=10)
                customtkinter.CTkLabel(frame_data, text=productname).grid(row=sno,column=2,padx=10,pady=10)
                customtkinter.CTkButton(frame_data,text='➖',width=5,height=4,command=lambda a=sno:removeqty(a)).grid(row=sno,column=3)
                qty=customtkinter.CTkLabel(frame_data, text='1')
                qty.grid(row=sno,column=4,padx=10,pady=10)
                qty_ref_list.append(['',''])
                qty_ref_list[sno-1][0]=qty
                addqty_button=customtkinter.CTkButton(frame_data,text='➕',width=5,height=4,command=lambda a=sno:addqty(a))
                addqty_button.grid(row=sno,column=5)
                price_label=customtkinter.CTkLabel(frame_data, text=f'Rs. {price}')
                price_label.grid(row=sno,column=6,padx=10,pady=10)
                qty_ref_list[sno-1][1]=price_label
                product_data[0]=sno
                product_data[1]=productname
                product_data[2]=1
                product_data[3]=float(price)
                data.append(product_data.copy())
                sno += 1
                sum+=price
                customtkinter.CTkLabel(frame_total,text=str(sum)).grid(row=0,column=1)

    root.after(16,update_cam)
update_cam()

root.mainloop()