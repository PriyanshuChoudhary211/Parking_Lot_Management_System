# Necessary Libraries
from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
from datetime import date
from flask import send_file
from datetime import timedelta
import pandas as pd
app=Flask(__name__)
import cv2
import pickle
import cvzone
import numpy as np
import json
import sqlite3

# --------------------------------TEMPORARY WORK---------------------------

# def temp():
    # db=sqlite3.connect("slotData.sqlite")
    # cur=db.cursor()
    # statement = '''SELECT * FROM slotBooking'''
    # cur.execute(statement)
    # data = cur.fetchall()
    # now = datetime.now()
    # current_time = str(now.strftime("%H:%M"))
    # todayDate=now.strftime("%d-%m-%Y")
    # print(todayDate)

    # cur.execute('delete from slotBooking where tareek<?',(todayDate,))
    # cur.execute('delete from slotBooking where tareek=? and checkOut<?',(todayDate,current_time,))
    # db.commit()
    # db=sqlite3.connect("finalUserRecord.sqlite")
    # cur=db.cursor()
    # cur.execute('delete from userRecord')
    # db.commit()

    # cur.execute('delete from slotBooking')
    # cur.execute('Create table userInfo(name varchar(50),email varchar(50), password varchar(20))')
    # cur.execute('Insert into userInfo values("Priyanshu","choudharypriyanshu2002@gmail.com","1234")')
    # cur.execute('Insert into userInfo values("Mridul Gupta","mridulpal09@gmail.com","1334")')
    # cur.execute('Drop table userInfo')
    # db.commit()


    # lastSevenDays=[]
    # now = datetime.now()
    # for x in range(7):
    #   d = now - timedelta(days=x)
    #   lastSevenDays.append(d.strftime("%d/%m"))
    # statement = '''SELECT * FROM userRecord'''
    # cur.execute(statement)
    # data = cur.fetchall()

# ----------------------------IS OVERLAPPING FUNCTION---------------------------------------------------------------

name='user'
def isOverlapping(timeIntervals,currInterval):
    c=0
    for item in timeIntervals:
        if currInterval[0]==item[0] and currInterval[1]>=item[1] and currInterval[1]<=item[2]:
            c+=1 
        elif currInterval[0]==item[0] and currInterval[2]>=item[1] and currInterval[2]<=item[2]:
            c+=1
        elif currInterval[0]==item[0] and item[1]>=currInterval[1] and item[1]<=currInterval[2]:
            c+=1
        elif currInterval[0]==item[0] and item[2]>=currInterval[1] and item[2]<=currInterval[2]:
            c+=1
        
    return c

#--------------------------------All USERS LIST---------------------------------------------------

@app.route('/allUsers')
def allUsers():
    path='C://Users//lenovo//Desktop//Parking Lot//python//allUsers.xlsx'
    return send_file(path, as_attachment=True)

#----------------------------------SLOT REPORT----------------------------------------------

@app.route('/slotReport')
def slotReport():
    path='C://Users//lenovo//Desktop//Parking Lot//python//slotReport.xlsx'
    return send_file(path, as_attachment=True)

#-----------------------------------SLOT BOOK---------------------------------------------------

@app.route('/slotBook',methods=['GET','POST'])
def slotBook():
    if request.method=='POST':
        db=sqlite3.connect("finalUserRecord.sqlite")
        cur=db.cursor()
        # cur.execute('create table userRecord(fullName varchar(20), carNo varchar(10), phoneNo varchar(15),checkIn varchar(15),checkOut varchar(15),amount varchar(10))') 
        fName=request.form.get('fName') 
        lName=request.form.get('lName') 
        carNo=request.form.get('carNo') 
        phone=request.form.get('phoneNumber') 
        t1=int(request.args.get('t1'))
        m1=int(request.args.get('m1'))
        t2=int(request.args.get('t2'))
        m2=int(request.args.get('m2'))
        print(t1,m1,t2,m2)
        tt1=str(t1)
        mm1=str(m1)
        tt2=str(t2)
        mm2=str(m2)
        if(t1<=9):
            tt1='0'+str(t1)
        if(m1<=9):
            mm1='0'+str(m1)
        if(t2<=9):
            tt2='0'+str(t2)
        if(m2<=9):
            mm2='0'+str(m2)
        checkIn=tt1+':'+mm1
        checkOut=tt2+':'+mm2
        price=request.args.get('amount')
        print(fName,lName,carNo,phone,checkIn,checkOut,price)
        c_name=fName+' '+lName
        cur.execute('insert into userRecord values(?,?,?,?,?,?)',(c_name,carNo,phone,checkIn,checkOut,price))
        db.commit()
    return render_template('slotBook.html')

#--------------------------------------USER-----------------------------------------------

@app.route('/user',methods=['GET','POST'])
def user():
    print('OutSide Request')
    # cur.execute('create table slotBooking(tareek varchar(20),checkIn varchar(10), checkOut varchar(10))')
    status=0
    checkIn='00:00:00'
    checkOut='00:00:00'
    if request.method=='POST':
        date=request.form.get('date')
        date=datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
        checkIn=request.form.get('checkIn')
        checkOut=request.form.get('checkOut')
        print(checkIn,checkOut)
        t1=int(checkIn[0])*10+int(checkIn[1])
        m1=int(checkIn[3])*10+int(checkIn[4])
        t2=int(checkOut[0])*10+int(checkOut[1])
        m2=int(checkOut[3])*10+int(checkOut[4])
        checkIn_time=datetime.strptime(checkIn,"%H:%M")
        checkOut_time=datetime.strptime(checkOut,"%H:%M")
        differenceSecond=checkOut_time-checkIn_time
        totalDifferenceSeconds=abs(differenceSecond.total_seconds())
        totalDifferenceHours=abs(totalDifferenceSeconds/(60*60))
        amount=totalDifferenceHours*20
        name=request.args.get('name')
        currInterval = [date,checkIn,checkOut]
        db=sqlite3.connect("slotData.sqlite")
        cur=db.cursor()
        statement = '''SELECT * FROM slotBooking'''
        cur.execute(statement)
        data = cur.fetchall()
        timeList=data
        now = datetime.now()
        current_time = str(now.strftime("%H:%M"))
        todayDate=now.strftime("%d-%m-%Y")
        print(todayDate)
        cur.execute('delete from slotBooking where tareek<?',(todayDate,))
        cur.execute('delete from slotBooking where tareek=? and checkOut<?',(todayDate,current_time,))
        db.commit()
        if isOverlapping(timeList,currInterval)>=20:
            status = 1
            return render_template('user.html',status=status)
        else:
            cur.execute('insert into slotBooking values(?,?,?)',(date,checkIn,checkOut))
            db.commit()
            # return render_template('slotBook.html',amount=amount)
            amount=format(amount,".2f")
            return redirect(url_for('slotBook',amount=amount,t1=t1,m1=m1,t2=t2,m2=m2,name=name))
    return render_template('user.html')

#--------------------------------------ADMIN-----------------------------------

@app.route('/admin')
def admin():
    db=sqlite3.connect("finalUserRecord.sqlite")
    cur=db.cursor()
    statement = '''SELECT * FROM userRecord'''
    cur.execute(statement)
    data = cur.fetchall()
    d=pd.read_sql_query("Select * from userRecord",db)
    d.to_excel('allUsers.xlsx')
    
    # Converting slotBooked Data into xlsx file
    db2=sqlite3.connect("slotData.sqlite")
    cur2=db2.cursor()
    now = datetime.now()
    current_time = str(now.strftime("%H:%M"))
    todayDate=now.strftime("%d-%m-%Y")
    print(todayDate)
    cur2.execute('delete from slotBooking where tareek<?',(todayDate,))
    cur2.execute('delete from slotBooking where tareek=? and checkOut<?',(todayDate,current_time,))
    db2.commit()
    d2=pd.read_sql_query("Select * from slotBooking",db2)
    d2.to_excel('slotReport.xlsx')

    #Last 7 days calculation
    lastSevenDays=[]
    now = datetime.now()
    for x in range(7):
        d = now - timedelta(days=x)
        lastSevenDays.append(d.strftime("%d/%m"))
    lastSevenDays.reverse()
    userList=[]
    for row in data:
        temp={'user':row[1],'ArrivalTime':row[3],'DepartureTime':row[4],'Amount':row[5]}
        userList.append(temp)
    userList = json.dumps(userList)
    # print(userList)
    return render_template('admin.html',userList=userList,lastSevenDays=lastSevenDays)

#------------------------------------- SIGN IN ---------------------------------------
status=0
@app.route('/signIn',methods=['GET','POST'])
def signIn():
    if request.method=='POST':
        check=0
        useremail=request.form.get('email')
        password=request.form.get('password')
        user=request.form.get('login')
        # user=request.form.get('login')
        # print(user)
        db=sqlite3.connect("register.sqlite")
        cur=db.cursor()
        statement = '''SELECT * FROM userInfo'''
        cur.execute(statement)
        data = cur.fetchall()

        # FOR ADMIN
        if useremail=='choudharypriyanshu2002@gmail.com' and password=='admin':
            return redirect(url_for('admin'))
        else:
        # FOR USER
            for row in data:
                if row[1]==useremail and row[2]==password and user=='on':
                    check=1
                    name=row[0]
        if check == 1:
            return redirect(url_for('user',name=name))
        db.commit()
    return render_template('signIn.html',status=status)

#-------------------------------------- SIGN UP -------------------------------

@app.route('/',methods=['GET','POST'])
def signUp():
    # print("hello")
    status=0
    if request.method == 'POST':
        db=sqlite3.connect("register.sqlite")
        cur=db.cursor()
        # cur.execute('Create table userInfo(name varchar(50),email varchar(50), password varchar(20))')
        # cur.execute('insert into userInfo values("Priyanshu","choudharypriyanshu2002@gmail.com","1234")')
        # print("Hello")
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username," ",email," ",password)
        statement = '''SELECT * FROM userInfo'''
        cur.execute(statement)
        data = cur.fetchall()
        for row in data:
            if row[1]==email:
                status=1
        if status == 1:
            return render_template("signUp.html",status=status)
        else:
            cur.execute('insert into userInfo values(?,?,?)',(username,email,password))
            db.commit()
            return redirect(url_for('signIn'))
    return render_template('signUp.html',status=status)

#-------------------------------------- CAR PARK ---------------------------------
@app.route('/carArea')
def carArea():
    #for captuing the video
    cap=cv2.VideoCapture('carPark.mp4')

    width,height=107,48
    #Opening car position list
    with open('CarParkPos','rb')as f:
        posList=pickle.load(f)

        
    def checkParkingSpace(imgPro):
        
        spaceCounter=0
        for pos in posList:
            x,y=pos        
            imgCrop=imgPro[y:y+height,x:x+width]
    #         cv2.imshow(str(x*y),imgCrop)
            count=cv2.countNonZero(imgCrop)
            cvzone.putTextRect(img,str(count),(x,y+height-10),scale=1,thickness=1,offset=0 )
        
            if count<900:
                color=(0,255,0)
                thickness=4
                spaceCounter+=1
            else:
                color=(0,0,255)
                thickness=2
                
            cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)  
        
        cvzone.putTextRect(img,f'Free Spaces:{spaceCounter} Total Space: {len(posList)}',(100,50),scale=2,thickness=2,offset=20,colorR=(0,200,0)   )
        

    while True:
        
        if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        success, img=cap.read()
        
        imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
        imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
        
        imgMedian=cv2.medianBlur(imgThreshold,5)
        kernel=np.ones((3,3),np.uint8)
        imgDilate=cv2.dilate(imgMedian,kernel,iterations=1) 
        
        checkParkingSpace(imgDilate)
    #     for pos in posList:
        
                
        cv2.imshow("Image",img)
        
    #     cv2.imshow("ThresholdImage",imgThreshold)
    #     cv2.imshow("ThresholdImage",imgMedian)
    #     cv2.imshow("ImageDilate",imgDilate)
        key=cv2.waitKey(10)
        if key == 27:
            break
    cv2.destroyAllWindows()
    return redirect(url_for('admin'))
#---------------------------------------- MAIN -------------------------------- 

if __name__=="__main__":
    app.run(debug=True)