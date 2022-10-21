# โปรแกรมชำระเบี้ยประกันภัย

from tkinter import *
from tkinter import ttk    #เรียกใช้ Combobox
from tkinter.filedialog import * #เรียกใช้ tkinter.filedialog เพื่อให้ผู้ใช้เลือกไฟล์สลิปการโอนเงิน เพื่อเป็นหลักฐานในการชำระเงิน
from datetime import date,datetime, timedelta #เพื่อเรียกใช้เวลาปัจจุบัน
import calendar #เพื่อนำมาคำนวณวันเวลาในการชำระเงินรอบถัดไป
import csv

#หน้าจอหลัก ชื่อ main_page
main_page = Tk()
main_page.title("โปรแกรมชำระเบี้ยประกันภัย")

#กำหนดขนาดและตำแหน่งของหน้าจอ
main_page.geometry("525x600+300+0") # width x height + x + y

#Label header
header = Label(
    main_page,
    text="โปรแกรมชำระเบี้ยประกันภัย", 
    font="Kanit 30 bold")
header.grid(row=0,column=1,pady=10,sticky=N)

#code ส่วนที่ให้ผู้ใช้กรอกอายุเพื่อดูเบี้ยประกันภัยและอัตราการชำระเบี้ยประกันภัยตามอายุของผู้ใช้
#Label Sub header
sub_header = Label(
    main_page,
    text="กรอกข้อมูลส่วนตัวของคุณและผู้รับสิทธิ์", 
    font="Kanit 18 bold",
    fg = "#665A48"
    )
sub_header.grid(row=1,column=1,padx=5,pady=10)

#เมื่อผู้ใช้กดปุ่ม ประวัติส่วนตัวของคุณ จะทำการเรียกฟังกชัน user_profile
def goto_user_profile():
    try :

        name = str(inp_username.get())
        lastname = str(inp_userlastname.get())

        if name == '' or lastname == '' :
            inform_user = Label(main_page,text="กรุณากรอกข้อมูลให้ถูกต้อง",fg="red",font = "Kanit 15")
            inform_user.grid(row=15,column=1)
        else :
            #หน้า profile คือ หน้าที่แสดงประวัติส่วนตัว และ วันเวลาในการชำระเบี้ยประกันภัยรอบถัดไป
            user_profile = Tk()
            user_profile.title("ประวัติส่วนตัวของคุณ") 
            user_profile.geometry("1000x550+300+0")

            #Label header
            header = Label(
                user_profile,
                text="ประวัติส่วนตัวของคุณ", 
                font="Kanit 30 bold")
            header.grid(row=0,column=1,pady=10,sticky=N)
            filepath = "insurance_data_file.csv"
            n = 0
            topic = [
                "วันเวลาที่ชำระเบี้ยประกันภัย",
                "ชื่อจริงผู้ใช้",
                "นามสกุลผุ้ใช้",
                "ที่อยู่ของผู้ใช้",
                "ชื่อจริงผู้รับสิทธิ์",
                "นามสกุลผู้รับสิทธิ์",
                "อายุผู้รับสิทธิ์ (ปี)",
                "ประเภทประกันภัย",
                "ระดับแผนประกันภัย",
                "ระยะเวลาสัญญา (เดือน)",
                "อัตราการชำระเบี้ยประกันภัย (บาท/เดือน)"
                ]
            with open(filepath,"r",encoding="utf-8") as infile:
                user_datafile = csv.reader(infile,delimiter=",",quotechar="|")
                for row in user_datafile:
                    data = list(row)
                    if data[1] == name and data[2] == lastname:
                        for i in range(len(topic)):
                            an_lbs = 1 + n
                            create_topic_lbs = Label(user_profile,text=f"{topic[i]}",font = "Kanit 18")
                            create_topic_lbs.grid(row=an_lbs,column=0,sticky=W)

                            create_space = Label(user_profile,text=" : ",font = "Kanit 18")
                            create_space.grid(row=an_lbs,column=1)

                            create_info_lbs = Label(user_profile,text=f"{data[i]}",font = "Kanit 18")
                            create_info_lbs.grid(row=an_lbs,column=2,sticky=W)
                            n += 1
                    
                        create_topic_lbs = Label(user_profile,text=f"วันเวลาในการชำระเงินรอบถัดไป",font = "Kanit 18 bold",fg="red")
                        create_topic_lbs.grid(row=an_lbs+2,column=0,sticky=W)

                        create_space = Label(user_profile,text=" : ",font = "Kanit 18")
                        create_space.grid(row=an_lbs+2,column=1)

                        last_round_payment = f"{data[0]}"
                        last_round_date = last_round_payment[:10]
                        list_date = last_round_date.split("/")
                        day = int(list_date[0])
                        month = int(list_date[1])
                        year = int(list_date[2])
                        last_date = date(year,month,day)
                        dayinmonths = calendar.monthrange(last_date.year, last_date.month)[1]
                        next_round_payment = last_date + timedelta(days=dayinmonths)

                        create_info_lbs = Label(user_profile,text=f"{next_round_payment}",font = "Kanit 18",fg="red")
                        create_info_lbs.grid(row=an_lbs+2,column=2,sticky=W)

                        def next_payment():
                            open_file = askopenfilename()
                            global collect_payment_file
                            collect_payment_file = open_file
                            row.pop(11)
                            row.insert(11,collect_payment_file)

                            current_confirm_date = datetime.now()
                            current_confirm_date = current_confirm_date.strftime("%d/%m/%Y %H:%M:%S") #วัน / เดือน / ปี ชั่วโมง : นาที : วินาที
                            row.pop(0)
                            row.insert(0,current_confirm_date)

                            with open(filepath,"a",encoding="utf-8") as data_file:
                                write = csv.writer(data_file)
                                write.writerow(row)

                            display_payment = Label(user_profile,text="คุณได้เลือกไฟล์แล้ว",font = "Kanit 18 bold",fg="#749F82")
                            display_payment.grid(row=an_lbs+4,column=1,pady=5)

                        bt_payment = Button(user_profile,text="ชำระเงินรอบถัดไป",font = "Kanit 18",command=next_payment)
                        bt_payment.grid(row=an_lbs+3,column=1,pady=5)

                        bt_backtpage = Button(user_profile,text="ย้อนกลับ",font = "Kanit 18",command=user_profile.destroy)
                        bt_backtpage.grid(row=an_lbs+3,column=0,pady=5)

                        user_profile.mainloop()

                        break
                    else:
                        pass
                 
    except IOError :
        inform_user = Label(main_page,text="กรุณากรอกข้อมูลให้ถูกต้อง",fg="red",font = "Kanit 15")
        inform_user.grid(row=15,column=1)

#คำนวณอัตราการชำระเบี้ยประกันภัยตามอายุผู้ใช้
def check_pay_rate(age):
    #อัตราการชำระเงินเริ่มต้น
    begin_pay= 1100
    pay_rate = begin_pay
    #อายุเริ่มต้นที่สามารถชำระเบี้ยประกันได้
    begin_age = 18

    while begin_age <= age:
        #print(f"pay insurance : {user_pay_rate} , age : {begin_age}") # print เพื่อตรวจสอบว่าเงื่อนไขถูกต้องหรือไม่
        if age == begin_age:
            break
        else:        
            begin_pay += 50
            begin_age += 1
            pay_rate = begin_pay

    return pay_rate

#ประเภทประกันชีวิต
type_insurance = ["ประกันชีวิต","ประกันอุบัติเหตุ","ประกันสุขภาพ"]
#ระดับแผนประกันชีวิต
level_insurance = ["ระดับที่1","ระดับที่2","ระดับที่3"]
#ระยะเวลาสัญญาการคุ้มครองประกันภัย
assurance_time = [3,6,12]

bt_confirm_dict = {}
bt_info_dict = {}

#หน้าที่ 3 : ชำระเบี้ยประกันภัย
def user_info(user_select):
    print(user_select) # เพื่อตรวจสมาชิกภายใน user_select ที่เก็บค่าต่างๆที่ผู้ใช้เลือก เมื่อผู้ใช้กดปุ่มยืนยัน
    
    info_page =Tk()
    info_page.title("ชำระเบี้ยประกันภัย")

    #กำหนดขนาดและตำแหน่งของหน้าจอ
    info_page.geometry("700x475+300+0") # width x height + x + y
    
    #ชำระเงิน
    def payment():
        open_file = askopenfilename()
        global collect_payment_file
        collect_payment_file = open_file
        display_payment = Label(info_page,text="คุณได้เลือกไฟล์แล้ว",font = "Kanit 18 bold",fg="#749F82")
        display_payment.grid(row=12,column=2,sticky=W)

    #กลับสู่หน้าหลัก
    def goto_mainpage():
        complete_page.destroy()
        info_page.destroy()
        insurance_page.destroy()
        
    #บันทึกข้อมูลของผู้ใช้
    def save_data():
        filepath = "insurance_data_file.csv"

        '''
        user_personal_data = {
        "ชื่อจริงของคุณ" : name,
        "นามสกุลของคุณ" : lastname,
        "ที่อยู่ของคุณ" : address,
        "ชื่อผู้รับสิทธิ์" : name_pssor,
        "นามสกุลผู้รับสิทธิ์" : lastname_pssor,
        "อายุผู้รับสิทธิ์" : age_pssor
        }
        '''
        #user_select = {ประเภทประกันภัย : [ระดับแผนประกันภัย,ระยะเวลาสัญญาการคุ้มครอง,อัตราการชำระเบี้ยประกันต่ออายุของผู้ใช้]}
        
        #row = [วันเวลาที่ยืนยันข้อมูล,ชื่อจริงผู้ใช้,นามสกุลผุ้ใช้,ที่อยู่ของผู้ใช้,ชื่อจริงผู้รับสิทธิ์,นามสกุลผู้รับสิทธิ์,อายุผู้รับสิทธิ์,ประเภทประกันภัย,ระดับแผนประกันภัย,ระยะเวลาสัญญา,อัตราการชำระเบี้ยประกันภัย,หลักฐานการโอนเงิน]
        row = []
        current_confirm_date = datetime.now()
        current_confirm_date = current_confirm_date.strftime("%d/%m/%Y %H:%M:%S") #วัน / เดือน / ปี ชั่วโมง : นาที : วินาที
        row.append(current_confirm_date)

        for values in user_personal_data.values():
            row.append(values)


        for key in user_select.keys():
            row.append(key)
            for values in user_select.values():
                for i in range(3):
                    row.append(values[i])
                    i += 1
        row.append(collect_payment_file)
        print(row) #print เพื่อตรวจสอบสมาชิกภาพใน row
        
        with open(filepath,"a",encoding="utf-8") as data_file:
            write = csv.writer(data_file)
            write.writerow(row)
        
        global complete_page
        complete_page = Tk()
        complete_page.title("ดำเนินการเสร็จสิ้น")
        complete_page.geometry("250x100+450+200")
        
        header = Label(complete_page,text="ดำเนินการเสร็จสิ้น",font = "Kanit 30 bold",fg="#665A48")
        header.grid(row=0,column=0,sticky=N,pady=5,padx=10)

        bt_mainpage = Button(complete_page,text="กลับสู่หน้าหลัก",font = "Kanit 18",command=goto_mainpage)
        bt_mainpage.grid(row=1,column=0,sticky=N)


    #header label
    header = Label(info_page,text="ชำระเบี้ยประกันภัย",font = "Kanit 30 bold",fg="#665A48")
    header.grid(row=0,column=0,sticky=N)

    #sub-header label
    sub_header = Label(info_page,text="ข้อมูลส่วนตัวของคุณ",font="Kanit 18 bold",fg = "#665A48")
    sub_header.grid(row=1,column=0,sticky=W)

    '''
    สร้าง Label ข้อมูลส่วนตัว
    ลำดับเลขคณิต an = a1 + (n-1)d
    a1 = 2
    d = 1
    ดังนั้น an = 1 + n
    '''
    n = 1
    
    
    #สร้าง Label ข้อมูลส่วนตัวจากการดึงข้อมูล key และ values ใน user_personal_data 
    for key,values in user_personal_data.items():
        an_lbs = 1 + n
        create_topic_lbs = Label(info_page,text=f"{key:20}",font = "Kanit 18")
        create_topic_lbs.grid(row=an_lbs,column=0,sticky=W)

        create_space = Label(info_page,text=" : ",font = "Kanit 18")
        create_space.grid(row=an_lbs,column=1)

        create_info_lbs = Label(info_page,text=f"{values}",font = "Kanit 18")
        create_info_lbs.grid(row=an_lbs,column=2,sticky=W)
        n += 1
    
    m = 0
    while m <= 6 :
        next_row = an_lbs +m

        if m == 0:
            sub_header = Label(info_page,text="ข้อมูลประกันภัยของคุณ",font = "Kanit 18 bold",fg="#665A48")
            sub_header.grid(row=next_row,column=0,sticky=W)
        elif m == 1:
            Label(info_page,text=f"ประเภทประกันภัย",font = "Kanit 18").grid(row=next_row,column=0,sticky=W)
            Label(info_page,text=" : ").grid(row=next_row,column=1)
            for key in user_select.keys():
                Label(info_page,text=f"{key}",font = "Kanit 18").grid(row=next_row,column=2,sticky=W)
        elif m == 2:
            Label(info_page,text="ระดับแผนประกันภัย",font = "Kanit 18").grid(row=next_row,column=0,sticky=W)
            Label(info_page,text=" : ").grid(row=next_row,column=1)
            for list in user_select.values():
                    Label(info_page,text=f"{list[0]}",font = "Kanit 18").grid(row=next_row,column=2,sticky=W)
        elif m == 3:
             Label(info_page,text="ระยะเวลาการคุ้มครองประกันภัย",font = "Kanit 18").grid(row=next_row,column=0,sticky=W)
             Label(info_page,text=" : ").grid(row=next_row,column=1)
             for list in user_select.values():    
                Label(info_page,text=f"{list[1]} เดือน",font = "Kanit 18").grid(row=next_row,column=2,sticky=W)
        elif m == 4:
            Label(info_page,text="อัตราการชำระเบี้ยประกันภัย",font = "Kanit 18").grid(row=next_row,column=0,sticky=W)
            Label(info_page,text=" : ").grid(row=next_row,column=1)
            for list in user_select.values():
                Label(info_page,text=f"{list[2]} บาท / เดือน",font = "Kanit 18").grid(row=next_row,column=2,sticky=W)
        elif m == 5:
            bt_payment = Button(info_page,text="ชำระเงิน",command=payment,width=10,font = "Kanit 18")
            bt_payment.grid(row=next_row,column=0,sticky=W)
        else:
            bt_savedata = Button(info_page,text="ยืนยัน",command=save_data,width=10,font = "Kanit 18")
            bt_savedata.grid(row=next_row,column=0,sticky=W)
            bt_backpage = Button(info_page,text="ย้อนกลับ",command=info_page.destroy,width=10,font = "Kanit 18")
            bt_backpage.grid(row=next_row,column=2,sticky=W)
            
        m += 1

    info_page.mainloop()
    
#ตรวจสอบอายุของผู้ใช้และแสดงประกันภัยแต่ละประเภท
def show_insurance():
    try:
        age_pssor = int(inp_age.get())
        name = str(inp_name.get())
        address = str(inp_address.get())
        lastname = str(inp_lastname.get())
        name_pssor = str(inp_name_pssor.get())
        lastname_pssor = str(inp_lastname_pssor.get())

        if age_pssor <= 0 or age_pssor == '' or name == '' or lastname == '' or address == '' or name_pssor == '' or lastname_pssor == '' or age_pssor == '' :
            raise ValueError()
        else:
            pass

    except:
        inform_user = Label(main_page,text="กรุณากรอกข้อมูลให้ถูกต้อง",fg="red",font = "Kanit 15")
        inform_user.grid(row=9,column=1)
    else:
        global user_personal_data
        user_personal_data = {
        "ชื่อจริงของคุณ" : name,
        "นามสกุลของคุณ" : lastname,
        "ที่อยู่ของคุณ" : address,
        "ชื่อผู้รับสิทธิ์" : name_pssor,
        "นามสกุลผู้รับสิทธิ์" : lastname_pssor,
        "อายุผู้รับสิทธิ์" : age_pssor
        }
        print(user_personal_data) #print เพื่อตรวจสอบสมาชิกใน user_personal_data

        Label(main_page,width=30).grid(row=9,column=1) 
        if age_pssor < 18 and age_pssor > 0 :
            Label(main_page,text="คุณอายุต่ำกว่า 18 ปี",fg="red",font = "Kanit 15").grid(row=9,column=1)
        elif age_pssor >= 18:
            #หน้าที่ 2 : ผู้ใช้เลือกประเภทประกันภัย
            global insurance_page
            insurance_page = Tk()
            insurance_page.title("เลือกประกันภัย")
            #กำหนดขนาดและตำแหน่งของหน้าจอ
            insurance_page.geometry("650x750+300+0") # width x height + x + y
            
            #
            global insurance_values
            insurance_values = {}

            user_pay_rate = check_pay_rate(age_pssor)
            global price_insurance
            #อัตราการชำระเบี้ยประกันภัยในแต่่ละระดับ [ระดับ 1,ระดับ 2,ระดับ 3]
            price_insurance = [user_pay_rate, user_pay_rate*1.5, user_pay_rate*2]

            Label(insurance_page,text="กรุณาเลือกประเภทประกันภัย",
            font = "Kanit 30 bold",
            fg="#665A48").grid(row=0,column=1)
            '''
            สร้าง label ประเภทประกันภัย ระดับ อัตราการชำระเบี้ยประกันภัย 
            ลำดับเลขคณิต an = a1 + (n-1)d

            a1 = 1
            d = 2
            ดังนั้น an = -1 + 2n 
            ดังนั้น an_label = (-1)+2*(k+1) เนื่องจาก k เริ่มจาก 0 
                
            สร้าง button ยืนยัน และ รายละเอียด
            a1 = 2
            d = 2
            ดังนั้น an = 2n
            ดังนั้น an_bt = 2*n เนื่องจาก n เริ่มจาก 1
            '''

            k = 0
            for i in range(len(type_insurance)): 
                for j in range(len(level_insurance)):
                    #สร้าง Label ชื่อประเภทประกันภัย ระดับแผนประกันภัย และอัตราการชำระเบี้ยต่ออายุของผู้ใช้ ในแถวที่ 1 ไปจนถึงแถวที่ n 
                    an_label = (-1)+2*(k+1)
                    create_lbs = Label(insurance_page,text=type_insurance[i],font = "Kanit 18")
                    create_lbs.grid(row=an_label,column=0)
                    create_level_lbs = Label(insurance_page,text=f"แผนประกันภัย{level_insurance[j]}",font = "Kanit 18")
                    create_level_lbs.grid(row=an_label,column=1)
                    create_pay_lbs = Label(insurance_page,text=f"{price_insurance[j]} บาท/เดือน",font = "Kanit 18")
                    create_pay_lbs.grid(row=an_label,column=2)       
                    k += 1

                    #เก็บค่าประเภทประกันภัย ระดับแผนประกันภัย ระยะเวลาสัญญาการคุ้มครอง และ อัตราการชำระเบี้ยประกันต่ออายุของผู้ใช้
                    insurance_values[k] = {type_insurance[i] : [level_insurance[j], assurance_time[j],price_insurance[j]]}
                    #print(insurance_values[k]) #print เพื่อตรวจสมาชิกภายใน insurance_values
            
                    for n in insurance_values:
                        #เพื่อรับค่าเมื่อผู้ใช้กดปุ่มยืนยันการเลือกประกันภัย
                        def select_values(m=n):
                            user_select = insurance_values[m]
                            #print(user_select) # เพื่อตรวจสมาชิกภายใน user_select ที่เก็บค่าต่างๆที่ผู้ใช้เลือก เมื่อผู้ใช้กดปุ่มยืนยัน
                            if __name__ == "__main__":
                                user_info(user_select)

                        def more_info(m=n):
                            if m <= 3:
                                #ประกันชีวิต
                                dt_1 = Tk()
                                dt_1.title('รายละเอียดประกัน')
                                dt_1.geometry('700x250+450+200')

                                dt11 = Label(dt_1,text='ประกันชีวิต',font=20).grid(row=0,column=2)
                                dt22 = Label(dt_1,text='แบบที่ 1',font=10).grid(row=1,column=1,padx=10)
                                dt33 = Label(dt_1,text='แบบที่ 2',font=10).grid(row=1,column=2,padx=10)
                                dt44 = Label(dt_1,text='แบบที่ 3',font=10).grid(row=1,column=3,padx=10)

                                dtt22 = Label(dt_1,text='ระยะเวลาความคุ้มครอง \n  10 ปี \n รับความคุ้มครอง \n 100,000 \n ชำระเบี้ยประกันภัย 5 ปี \n กรณีเสียชีวิตรับความคุ้มครอง \n 100,000 \n ชำระเบี้ยประกันครบ \n และเลยระยะเวลาความคุ้มครองได้รับ \n 150,000').grid(row=2,column=1,padx=10)
                                dtt33 = Label(dt_1,text='ระยะเวลาความคุ้มครอง \n  15 ปี \n รับความคุ้มครอง \n 150,000 \n ชำระเบี้ยประกันภัย 8 ปี \n กรณีเสียชีวิตรับความคุ้มครอง \n 150,000 \n ชำระเบี้ยประกันครบ \n และเลยระยะเวลาความคุ้มครองได้รับ \n 200,000').grid(row=2,column=2,padx=10)
                                dtt44 = Label(dt_1,text='ระยะเวลาความคุ้มครอง \n  20 ปี \n รับความคุ้มครอง \n 200,000 \n ชำระเบี้ยประกันภัย 10 ปี \n กรณีเสียชีวิตรับความคุ้มครอง \n 200,000 \n ชำระเบี้ยประกันครบ \n และเลยระยะเวลาความคุ้มครองได้รับ \n 300,000').grid(row=2,column=3,padx=10)

                                def backpg():
                                    dt_1.destroy()

                                bkp = Button(dt_1,text='Back',width=6,command=backpg).grid(row=3,column=2,pady=10)

                                dt_1.mainloop()
                            elif m <= 6 :
                                #ประกันอุบัติเหตุ
                                dt_2 = Tk()
                                dt_2.title('รายละเอียดประกัน')
                                dt_2.geometry('800x250+450+200')

                                dt111 = Label(dt_2,text='ประกันอุบัติเหตุ',font=20).grid(row=0,column=2)
                                dt222 = Label(dt_2,text='แบบที่ 1',font=10).grid(row=1,column=1,padx=10)
                                dt333 = Label(dt_2,text='แบบที่ 2',font=10).grid(row=1,column=2,padx=10)
                                dt444 = Label(dt_2,text='แบบที่ 3',font=10).grid(row=1,column=3,padx=10)

                                dtt22 = Label(dt_2,text='ระยะเวลาความคุ้มครอง \n  1 ปี \n รับความคุ้มครอง \n 200,000 \n กรณีเสียชีวิตการเสียชีวิตจากอุบัติเหตุทั่วไป \n ถูกฆาตกรรมรับความคุ้มครอง \n 200,000 \n ค่ารักษาพยาบาล(ต่ออุบัติเหตุ) \n 10,000').grid(row=2,column=1,padx=10)
                                dtt33 = Label(dt_2,text='ระยะเวลาความคุ้มครอง \n  1 ปี \n รับความคุ้มครอง \n 350,000 \n กรณีเสียชีวิตการเสียชีวิตจากอุบัติเหตุทั่วไป \n ถูกฆาตกรรมรับความคุ้มครอง \n 350,000 \n ค่ารักษาพยาบาล(ต่ออุบัติเหตุ) \n 20,000').grid(row=2,column=2,padx=10)
                                dtt44 = Label(dt_2,text='ระยะเวลาความคุ้มครอง \n  1 ปี \n รับความคุ้มครอง \n 500,000 \n กรณีเสียชีวิตการเสียชีวิตจากอุบัติเหตุทั่วไป \n ถูกฆาตกรรมรับความคุ้มครอง \n 500,000 \n ค่ารักษาพยาบาล(ต่ออุบัติเหตุ) \n 30,000').grid(row=2,column=3,padx=10)



                                def backpg():
                                    dt_2.destroy()

                                bkp = Button(dt_2,text='Back',width=6,command=backpg).grid(row=3,column=2,pady=10)

                                dt_2.mainloop()
                            
                            else:
                                #ประกันสุขภาพ
                                dt = Tk()
                                dt.title('รายละเอียดประกัน')
                                dt.geometry('575x250+450+200')

                                dt1 = Label(dt,text='ประกันสุขภาพ',font=20).grid(row=0,column=2)
                                dt2 = Label(dt,text='แบบที่ 1',font=10).grid(row=1,column=1,padx=10)
                                dt3 = Label(dt,text='แบบที่ 2',font=10).grid(row=1,column=2,padx=10)
                                dt4 = Label(dt,text='แบบที่ 3',font=10).grid(row=1,column=3,padx=10)

                                dtt2 = Label(dt,text='ระยะเวลาความคุ้มครอง \n ถึงอายุ 80 ปี \n รับความคุ้มครอง \n 500,000 \n การเข้ารักษาในโรงพยาบาล \n จ่ายตามจริง \n กรณีเสียชีวิตรับความคุ้มครอง \n 150,000').grid(row=2,column=1,padx=10)
                                dtt3 = Label(dt,text='ระยะเวลาความคุ้มครอง \n ถึงอายุ 80 ปี \n รับความคุ้มครอง \n 1,000,000 \n การเข้ารักษาในโรงพยาบาล \n จ่ายตามจริง \n กรณีเสียชีวิตรับความคุ้มครอง \n 150,000').grid(row=2,column=2,padx=10)
                                dtt4 = Label(dt,text='ระยะเวลาความคุ้มครอง \n ถึงอายุ 80 ปี \n รับความคุ้มครอง \n 1,500,000 \n การเข้ารักษาในโรงพยาบาล \n จ่ายตามจริง \n กรณีเสียชีวิตรับความคุ้มครอง \n 150,000').grid(row=2,column=3,padx=10)



                                def backpg():
                                    dt.destroy()

                                bkp = Button(dt,text='Back',width=6,command=backpg).grid(row=3,column=2,pady=10)

                                dt.mainloop()


                        #สร้างปุ่มยืนยันและรายละเอียด ในแถวที่ 2 ไปจนถึงแถวที่ n 
                        an_bt = 2*n
                        bt_confirm_dict[n] = Button(insurance_page,text="ยืนยัน",command=select_values,width=6,padx=2,font = "Kanit 18")
                        bt_confirm_dict[n].grid(row=an_bt,column=0,pady=5)
                        bt_info_dict[n] = Button(insurance_page,text="รายละเอียดเพิ่มเติม",width =10,font = "Kanit 18",command=more_info)
                        bt_info_dict[n].grid(row=an_bt,column=1,pady=5)  

            bt_backpage = Button(insurance_page,text="ย้อนกลับ",command=insurance_page.destroy,width=8,font = "Kanit 18")
            bt_backpage.grid(row=an_bt+1,column=1) 

            insurance_page.mainloop()

#ตัวแปรที่ใช้เก็บข้อมูลเมื่อผู้ใช้กรอกข้อมูลเข้ามา
inp_age = StringVar()
inp_name = StringVar()
inp_lastname = StringVar()
inp_address = StringVar()
inp_name_pssor = StringVar()
inp_lastname_pssor = StringVar()

#ชื่อของผู้ใช้
lb_name = Label(main_page,text="ชื่อจริงของคุณ",font = "Kanit 18")
lb_name.grid(row=2,column=0,sticky=W)

ent_name = Entry(main_page,textvariable=inp_name,width=25,font = "Kanit 15")
ent_name.grid(row=2,column=1)
ent_name.focus()

#นามสกุลของผู้ใข้
lb_lastname = Label(main_page,text="นามสกุลของคุณ",font = "Kanit 18")
lb_lastname.grid(row=3,column=0,sticky=W)

ent_lastname = Entry(main_page,textvariable=inp_lastname,width=25,font = "Kanit 15")
ent_lastname.grid(row=3,column=1)

#ที่อยู่
lb_address = Label(main_page,text="ที่อยู่ของคุณ",font = "Kanit 18")
lb_address.grid(row=4,column=0,sticky=W)

ent_address = Entry(main_page,textvariable=inp_address,width=25,font = "Kanit 15")
ent_address.grid(row=4,column=1)

#ชื่อผู้รับสิทธิ์
lb_name_pssor = Label(main_page,text="ชื่อผู้รับสิทธิ์",font = "Kanit 18")
lb_name_pssor.grid(row=5,column=0,sticky=W)

ent_name_pssor = Entry(main_page,textvariable=inp_name_pssor,width=25,font = "Kanit 15")
ent_name_pssor.grid(row=5,column=1)

#นามสกุลผู้รับสิทธิ์
lb_lastname_pssor = Label(main_page,text="นามสกุลผู้รับสิทธิ์",font = "Kanit 18")
lb_lastname_pssor.grid(row=6,column=0,sticky=W)

ent_lastname_pssor = Entry(main_page,textvariable=inp_lastname_pssor,width=25,font = "Kanit 15")
ent_lastname_pssor.grid(row=6,column=1)

#อายุของผู้รับสิทธิ์
lb_age = Label(main_page,text="อายุของผู้รับสิทธิ์",font = "Kanit 18")
lb_age.grid(row=7,column=0,sticky=W)

ent_age = Entry(main_page,textvariable=inp_age,width=25,font = "Kanit 15")
ent_age.grid(row=7,column=1,pady=5)

bt_confirm = Button(main_page,text="ยืนยัน",command=show_insurance,width=10,font = "Kanit 18")
bt_confirm.grid(row=8,column=1)

#Label Sub header
sub_header = Label(
    main_page,
    text="เลือกทำรายการอื่นๆ", 
    font="Kanit 30 bold",
    fg = "#665A48"
    )
sub_header.grid(row=10,column=1,padx=5,pady=10)

inp_username = StringVar()
inp_userlastname = StringVar()

lb_user_profile = Label(main_page,text="ประวัติส่วนตัวของคุณ",font = "Kanit 18",fg = "#665A48",width=15)
lb_user_profile.grid(row=11,column=1,pady=5)

#ชื่อผู้รับสิทธิ์
lb_name_pssor = Label(main_page,text="ชื่อจริงของคุณ",font = "Kanit 18")
lb_name_pssor.grid(row=12,column=0,sticky=W)

ent_name_pssor = Entry(main_page,textvariable=inp_username,width=25,font = "Kanit 15")
ent_name_pssor.grid(row=12,column=1)

#นามสกุลผู้รับสิทธิ์
lb_lastname_pssor = Label(main_page,text="นามสกุลของคุณ",font = "Kanit 18")
lb_lastname_pssor.grid(row=13,column=0,sticky=W)

ent_lastname_pssor = Entry(main_page,textvariable=inp_userlastname,width=25,font = "Kanit 15")
ent_lastname_pssor.grid(row=13,column=1)

bt_confirm = Button(main_page,text="ยืนยัน",command=goto_user_profile,width=10,font = "Kanit 18")
bt_confirm.grid(row=14,column=1)

main_page.mainloop()