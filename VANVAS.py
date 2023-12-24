#importing needed modules
from tkinter import *
from tkcalendar import *
import mysql.connector
from functools import partial
from tkinter import messagebox

#connecting to db
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="vanvas"
)

cal=None #variable for calender

#initializing db cursor
mycursor = mydb.cursor()
root=Tk()
root.title("VANVAS")
#root.iconbitmap('C:/Users/nihaa/Desktop/i1.ico')
root.geometry("440x410")
root.maxsize(440,410)
root.configure(bg='Black')

# Funtion to open new window
newWindow=None
def openNewWindow():
    global newWindow
    # Toplevel object which will be treated as a new window
    newWindow = Toplevel()
    newWindow.configure(bg='#567')
    #newWindow.iconbitmap('C:/Users/nihaa/Desktop/i1.ico')
    
#FUNCTIONS FOR MAIN PAGE

#1. ADD STUDENT FUNCTION
    
def AddStu():
    global newWindow
    openNewWindow() # opening new window
    # Setting dimensions of window and adding elements into the window
    newWindow.title("Add Student")
    newWindow.geometry('560x250')
    newWindow.maxsize(560,250) #setting maximum window size

    #creating elements required for entering data
    NameL= Label(newWindow,text='Enter Name : ',font=('Georgia','11','bold')).grid(pady=10,row=1,column=2)
    NameE=Entry(newWindow)
    NameE.grid(padx=9,pady=10,row=1,column=3)

    AdNoL= Label(newWindow,text='Enter Admission Number : ',font=('Georgia','11','bold')).grid(pady=10,row=2,column=2)
    AdNoE=Entry(newWindow)
    AdNoE.grid(padx=9,pady=10,row=2,column=3)
    
    ClassL= Label(newWindow,text='Enter Class : ',font=('Georgia','11','bold')).grid(pady=10,row=3,column=2)
    ClassE=Entry(newWindow)
    ClassE.grid(padx=9,pady=10,row=3,column=3)

    SecL= Label(newWindow,text='Enter Section : ',font=('Georgia','11','bold')).grid(pady=10,row=4,column=2)
    SecE=Entry(newWindow)
    SecE.grid(padx=9,pady=10,row=4,column=3)
    
    #buttons to save and cancel operation
    SaveB=Button(newWindow,text='SAVE',command=partial(SaveStudB,NameE,AdNoE,ClassE,SecE),font=('Georgia','10'))
    SaveB.grid(padx=30,pady=10,row=5,column=1)
    
    CancelB=Button(newWindow,text='CANCEL',command=newWindow.destroy,font=('Georgia','10'))
    CancelB.grid(padx=10,pady=10,row=5,column=4)

    
def SaveStudB(NameE,AdNoE,ClassE,SecE):# function for Saving Student into DB
    #showing message box to confirm addition of student
    MsgBoxChk=messagebox.askyesno("Confirm Addition",'Are you SURE you want to add this student?')
    
    if MsgBoxChk==True:
        mycursor.execute('insert into student_master values ('+AdNoE.get()+",\'"+NameE.get()+'\','+ClassE.get()+',\''+SecE.get()+'\')')
        mydb.commit()
        newWindow.destroy() #closing window after adding student
    else:
        newWindow.attributes('-topmost',True) # bringing the window to the top


#2. DELETE STUDENT FUNCTION
        
def DelStu():
    global newWindow
    openNewWindow() #opening new window
    #Setting dimensions of window and adding elements into the window
    newWindow.title("Delete Student")
    newWindow.geometry('355x170')
    newWindow.maxsize(355,170)
    
    #creating elements required for entering data
    AdnoL= Label(newWindow,text='Enter Admission Number : ',font=('Georgia','11')).grid(padx=10,pady=35,row=1,column=1)
    AdnoE=Entry(newWindow)
    AdnoE.grid(padx=10,pady=35,row=1,column=3)
    
    # buttons to check student and cancel operation
    ChkStB= Button(newWindow,text='Check Student',command=partial(ChkStudB,AdnoE))
    ChkStB.grid(padx=30,pady=10,row=4,column=1)
    
    CancelB=Button(newWindow,text='CANCEL',command=newWindow.destroy) #closing window
    CancelB.grid(padx=30,pady=10,row=4,column=3)

    
def ChkStudB(AdNoE): # function to check if student is in the DB and deleting if found.
    
    mycursor.execute('select * from student_master where admission_no='+AdNoE.get())
    StuData=None
    for data in mycursor:
        StuData=data #StuData is TUPLE of Values
    if StuData==None:
        # showing error box if student not present in DB
        messagebox.showerror('ERROR','Student does not exist. \nRetry with Valid Admission number.')
        newWindow.attributes('-topmost',True) # bringing window to the top
    else:
        MsgBoxChk=messagebox.askyesno("Confirm Deletion",str(StuData)+'\nAre you SURE you want to DELETE this student?')
        
        if MsgBoxChk==True:
            mycursor.execute('delete from student_master where admission_no ='+str(StuData[0]))
            mydb.commit()
            newWindow.destroy() #closing window 
        else:
            newWindow.attributes('-topmost',True) # bringing window to the top


#3. MARK ATTENDANCE FUNCTION
            
#initializing variables for filtering
Names=[] # name, admission number of student in selected Class and Section
NamesLabList=[] #List of labels of names and option menu in the window
ValueList=[] #list of values selected in option menu

def Filter(Class,Sec): #filters students based on selected class and section, and displays them on the window
    global cal, Names, NamesLabList, ValueList
    
    for i in NamesLabList:
        i[0].after(1, i[0].destroy())
        i[1].after(1, i[1].destroy()) #clearing older data from window
    NamesLabList.clear() #clearing the list
    mycursor.execute("Select Name,admission_no from student_master where class="+Class.get()+" and Section='"+Sec.get()+"';")
    Names=mycursor.fetchall()
    mycursor.execute("select S.name, A.p_a from student_master S, att_reg A where A.date='"+cal.get_date()+"' and A.admission_no=S.admission_no ;")
    Res=mycursor.fetchall()
    
    for i in range(len(Names)):       
        NameL=Label(newWindow,text=Names[i][0])
        NameL.grid(column=3,row=i+2)
        ValueInside=StringVar(newWindow)
        
        if Names[i][0] in [i[0] for i in Res]: # if name is there in att_reg
            mycursor.execute("Select p_a from att_reg where admission_no = "+str(Names[i][1])+" and date = '"+cal.get_date()+"';")
            p_a=mycursor.fetchone()
            ValueInside.set(p_a[0])    
        else: #if name not there in att_reg
            ValueInside.set('Present')
        OpMen=OptionMenu(newWindow,ValueInside,"Present","Absent")
        OpMen.grid(column=4,row=i+2)
        ValueList.append(ValueInside)
        NamesLabList.append((NameL,OpMen))


def SaveAtt(): # saving attendance to the DB
    Att_List=[] # list of values to be saved into DB
    global cal, Names, ValueList
    
    # sorting values to be saved into DB and putting into list
    for i in range (len(Names)):
        if "Present" in ValueList[i].get():
            Value= 'Present'
        else:
            Value= 'Absent'
        Att_List.append((Names[i][1],Value,cal.get_date())) 
    ValueList.clear()
    
    AdmNoList = tuple([i[0] for i in Att_List])
    mycursor.execute("Select * from att_reg where admission_no in "+ str(AdmNoList)+"and date='"+cal.get_date()+"' ;")
    OldRec=mycursor.fetchall()
    
    for i in OldRec: #checking if record already exists for that date and updating
        for j in Att_List: 
            if i[1] == j[0]:
                sql1="Update att_reg SET p_a = '"+j[1]+"' where date= '"+j[2]+"' and record_no = "+str(i[0])+";"
                mycursor.execute(sql1)
                mydb.commit()
                del Att_List[Att_List.index(j)]
    else: #if not present in DB, inserting record into DB.
        sql2='insert into att_reg (admission_no,p_a,date) values(%s,%s,%s)'
        mycursor.executemany(sql2,Att_List)
        mydb.commit()
    print('Attendance has been saved!')


def MarAtt(): #main function for marking attendance
    global newWindow
    global cal
    openNewWindow() #opening new window
    #Setting dimensions of window and adding elements into the window
    height=newWindow.winfo_screenheight()
    newWindow.geometry('750x'+str(height-100))
    newWindow.maxsize(750,height-65)
    newWindow.title("Mark Attendance")
    
    #Class section Selection
    ClassL= Label(newWindow,text='Enter Class : ',font=('Georgia','13')).grid(padx=10,pady=10,row=1,column=1)
    ClassE=Entry(newWindow)
    ClassE.grid(padx=10,pady=10,row=1,column=2)

    SecL= Label(newWindow,text='Enter Section : ',font=('Georgia','13')).grid(padx=10,pady=10,row=2,column=1)
    SecE=Entry(newWindow)
    SecE.grid(padx=10,pady=10,row=2,column=2)

    
    #Calender
    cal=Calendar(newWindow,selectmode="day",year=2022,month=1,day=1)
    cal.grid(column=1,row=4,rowspan=6,padx=10)
    
    NameL = Label(newWindow,text='Name',font=('Georgia','13')).grid(padx=80,pady=6,row=1,column=3)
    PAL = Label(newWindow,text='Attendance',font=('Georgia','13')).grid(padx=10,pady=6,row=1,column=4)
    
    # Buttons to display and save attendance
    SelectB=Button(newWindow,text='Select',command=partial(Filter,ClassE,SecE)).grid(padx=10,pady=10,row=3,column=2)

    SaveAttB= Button(newWindow, text='Save Attendance',command=lambda:[SaveAtt(),newWindow.destroy()]).grid(padx=10,pady=10, row=4, column=2)
        #using lambda function to call multiple functions.


#4. View Report
NamesLabList2=[] # list of Name labels , Total present and total absent values.

def SelectB2(Class,Sec,Month,Year): # filters students based on selected class and section, and displays them on the window
    for i in NamesLabList2:
        i[0].after(1, i[0].destroy())
        i[1].after(1, i[1].destroy())
        i[2].after(1, i[2].destroy()) #clearing older data from window
    NamesLabList2.clear() #clearing the list
    # getting data from DB 
    mycursor.execute("Select Name from student_master where class="+Class.get()+" and Section='"+Sec.get()+"';")
    Names=mycursor.fetchall()
    DateStr=Month.get()+"/%/"+Year.get()
    mycursor.execute("Select S.name, A.p_a from Student_master S, att_reg A where A.date like '"+DateStr+"' and A.admission_no=S.admission_no and S.Section= '"+Sec.get()+"' and S.Class='"+Class.get()+"' ;")
    Result=mycursor.fetchall()
    
    # sorting data
    for i in range(len(Names)):
        P=A=0
        for j in Result:
            if Names[i][0]==j[0]:
                if j[1]=='Present':
                    P+=1
                else:
                    A+=1
        #displaying the data on the window
        NameL=Label(newWindow,text=Names[i])
        NameL.grid(column=3,row=i+2)
        TP=Label(newWindow,text=str(P))
        TP.grid(column=4,row=i+2)
        TA=Label(newWindow,text=str(A))
        TA.grid(column=5,row=i+2)
        NamesLabList2.append((NameL,TP,TA)) #appending data into label list

    
def ViewReport(): #main function to view report
    
    global newWindow
    openNewWindow() #opening new window
    #Setting dimensions of window and adding elements into the window
    height=newWindow.winfo_screenheight()
    newWindow.geometry('750x'+str(height-100))
    newWindow.maxsize(750,height-65)
    newWindow.title("View Report")
    
    #Class section Selection
    ClassL= Label(newWindow,text='Enter Class : ',font=('Georgia','13')).grid(padx=10,pady=10,row=1,column=1)
    ClassE=Entry(newWindow)
    ClassE.grid(padx=10,pady=10,row=1,column=2)

    SecL= Label(newWindow,text='Enter Section : ',font=('Georgia','13')).grid(padx=10,pady=10,row=2,column=1)
    SecE=Entry(newWindow)
    SecE.grid(padx=10,pady=10,row=2,column=2)

    NameL = Label(newWindow,text='Name',font=('Georgia','13')).grid(padx=80,pady=6,row=1,column=3)
    PL = Label(newWindow,text='P Total',font=('Georgia','13')).grid(padx=10,pady=6,row=1,column=4)
    Al= Label(newWindow,text='A Total',font=('Georgia','13')).grid(padx=10,pady=6,row=1,column=5)

    #Option menus for selecting month and year.
    ValueInside2=StringVar(newWindow)
    ValueInside2.set('Select Month')
    MonOM= OptionMenu(newWindow,ValueInside2, '1','2','3','4','5','6','7','8','9','10','11','12')
    MonOM.grid(padx=10,pady=10, row=3,column=1)
    
    ValueInside3=StringVar(newWindow)
    ValueInside3.set('Select Year')
    YearOM= OptionMenu(newWindow, ValueInside3, '20','21','22')
    YearOM.grid(padx=10,pady=10, row=3,column=2)
    # button to display    
    SelectB=Button(newWindow,text='Select',command=partial(SelectB2, ClassE, SecE, ValueInside2, ValueInside3)).grid(padx=10,pady=10,row=4,column=2)


#BUTTONS FOR MAIN PAGE

TitleL=Label(root,text='VANVAS',font=('Gill Sans Ultra Bold',40),bg='Black',fg='White').grid(padx=5,pady=5,row=1,column=3)
#1.Add Student
Add_StB = Button(root,text='Add Student',command = AddStu,bg='Black',fg='White',font=('Georgia','13'),relief='groove')
Add_StB.grid(padx=142,pady=20,row=2,column=3)
#2.Delete Student
Del_StB = Button(root,text='Delete Student',command=DelStu,bg='Black',fg='White',font=('Georgia','13'),relief='groove')
Del_StB.grid(padx=142,pady=20,row=3,column=3)
#3.Mark Attendance
M_AttB = Button(root,text='Mark Attendance',command=MarAtt,bg='Black',fg='White',font=('Georgia','13'),relief='groove')
M_AttB.grid(padx=142,pady=20,row=4,column=3)
#4.View Report
V_RepB = Button(root,text='View Report',command=ViewReport,bg='Black',fg='White',font=('Georgia','13'),relief='groove')
V_RepB.grid(padx=142,pady=20,row=5,column=3)


