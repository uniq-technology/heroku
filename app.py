from flask import Flask,redirect,render_template,request,flash,url_for
import sqlite3
import os
import pickle
import numpy as np
import cv2
import os
import sqlite3 as sql

import sqlite3
app=Flask(__name__)

dbase=sqlite3.connect("static/database/lung.db")
dbase.execute('''

CREATE TABLE if not exists user (
  name text NOT NULL,
  password text NOT NULL,
  mail text NOT NULL,
  contact text NOT NULL,
  address text NOT NULL
)

''')
from tensorflow.keras.models import load_model
model_tuberculosis = load_model('model/tuberculosis_model.h5')

from tensorflow.keras.models import load_model
model_pneumonia = load_model('model/pneumonia_model.h5')

from tensorflow.keras.models import load_model
model_covid = load_model('model/covid_model.h5')

img_size=200

def closest(lst, K):
	
	lst = np.asarray(lst)
	idx = (np.abs(lst - K)).argmin()
	return lst[idx]

    
@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method=="POST":
        uname=request.form['uname']
        upass=request.form['pass']
        email=request.form['email']
        contact=request.form['contact']
        address=request.form['address']
        with sqlite3.connect('static/database/lung.db') as con:
            a=con.cursor()
            a.execute('insert into user (name,password,mail,contact,address) values (?,?,?,?,?)',(uname,upass,email,contact,address))
            con.commit()
            return  redirect(url_for('login'))
    return  render_template('register.html')

@app.route('/loginaction', methods=['POST'])
def loginaction():
    r=""
    if request.method=="POST":
        uname=request.form['name']
        upass=request.form['password']
        con=sqlite3.connect('static/database/lung.db')
        a=con.execute(" select * from user where name='" +uname+ "' and password='"+upass+"' ")
        r=a.fetchall()
        for i in r:
            if(uname==i[0] and upass==i[1]):
                return redirect(url_for("index"))
            else:
                flash("Invalid username or password","danger")
                return  render_template('login.html')
                

    
    return render_template("login.html")



@app.route('/result', methods=['POST'])
def result():
    if request.method=="POST":
        pin_code=int(request.form["pin"])
        print(pin_code)

        dbase=sqlite3.connect("static/database/Hospital_detail.db")
        con=dbase.cursor()
        con.execute("SELECT PIN_CODE FROM TAB1 ")
        data=con.fetchall()

        if data:
            data_list=[]
            for d in data:
                data_list.append(d[0])
                  
             #print(data_list)

        
        pin=closest(data_list, pin_code)
        print(pin)

        con.execute("SELECT * FROM TAB1 WHERE PIN_CODE =?",(int(pin),))
        total_data=con.fetchone()
        

        if total_data:
            print(total_data)
            print("Hospital Address:",total_data[2])
            print("Phone number:",total_data[3])
            print("Pin number:",total_data[1])
            Hd01=str(total_data[1])
            Hd02=str(total_data[2])
            Hd03=str(total_data[3])
            output11=str(total_data[2])
            output12=str(total_data[3])
        data_list.remove(pin)

        pin=closest(data_list, pin_code)
        print(pin)

        con.execute("SELECT * FROM TAB1 WHERE PIN_CODE =?",(int(pin),))
        total_data=con.fetchone()


        if total_data:
            print(total_data)
            print("Hospital Address:",total_data[2])
            print("Phone number:",total_data[3])
            print("Pin number:",total_data[1])
            Hd11=str(total_data[1])
            Hd12=str(total_data[2])
            Hd13=str(total_data[3])
            output21=str(total_data[2])
            output22=str(total_data[3])
        data_list.remove(pin)


        pin=closest(data_list, pin_code)
        print(pin)

        con.execute("SELECT * FROM TAB1 WHERE PIN_CODE =?",(int(pin),))
        total_data=con.fetchone()


        if total_data:
            print(total_data)
            print("Hospital Address:",total_data[2])
            print("Phone number:",total_data[3])
            print("Pin number:",total_data[1])
            Hd21=str(total_data[1])
            Hd22=str(total_data[2])
            Hd23=str(total_data[3])
            output31=str(total_data[2])
            output32=str(total_data[3])
        data_list.remove(pin)
        dbase.close()
        
        
        

        
        return render_template("result.html",Hd01=Hd01, Hd02=Hd02 ,Hd03=Hd03,Hd11=Hd11, Hd12=Hd12 ,Hd13=Hd13,Hd21=Hd21, Hd22=Hd22 ,Hd23=Hd23)


@app.route('/res')
def res():
    return render_template("result.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")  

@app.route('/reg')
def reg():
    return render_template("register.html")  



app.config["UPLOAD_FOLDER"]="static/images"
@app.route('/pincode', methods=['POST'])
def pincode():
    if request.method=="POST":
        upload_image=request.files["upload_image"]
        if upload_image.filename!='':
            filepath=os.path.join(app.config["UPLOAD_FOLDER"],upload_image.filename) 
            upload_image.save(filepath)
            flash("Image Uploaded Successfully","success")
            a=os.path.abspath(filepath)

            image_directory=a



            print(image_directory)
            if image_directory.endswith(".jpeg") == True or image_directory.endswith(".jpg") == True or image_directory.endswith(".png") == True:
                data1=[]


                try:
                    img=cv2.imread(image_directory,cv2.IMREAD_GRAYSCALE)
                    resizing=cv2.resize(img,(img_size,img_size))

                    data1.append(resizing)
                except Exception as e:
                    print(e)
                try_test=np.array(data1)
                try_test=np.array(try_test)/255

                try_test=try_test.reshape(-1,200,200,1)
                pred=[]
                def predict_prob(number):
                    return [number[0],1-number[0]]           

                prediction_tuberculosis=model_tuberculosis.predict(try_test)[0]
                print(prediction_tuberculosis)
                p_tuberculosis=max(np.array(list(map(predict_prob, model_tuberculosis.predict(try_test))))[0])
                print(p_tuberculosis)
                
                p1=1-p_tuberculosis if p_tuberculosis<0.5 else p_tuberculosis
                p1=round(p1*100,4)            

                prediction_tuberculosis_pred='TUBERCULOSIS' if prediction_tuberculosis<0.5 else 'NORMAL' 
                pred.append(prediction_tuberculosis_pred)


                prediction_pneumonia=model_pneumonia.predict(try_test)[0]
                print(prediction_pneumonia)
                p_pneumonia=max(np.array(list(map(predict_prob, model_pneumonia.predict(try_test))))[0])
                p2=1-p_pneumonia if p_pneumonia<0.5 else p_pneumonia
                p2=round(p2*100,4)            

                prediction_pneumonia_pred='PNEUMONIA' if prediction_pneumonia<0.5 else 'NORMAL' 
                pred.append(prediction_pneumonia_pred)


                prediction_covid=model_covid.predict(try_test)[0]
                print(prediction_covid)
                p_covid=max(np.array(list(map(predict_prob, model_covid.predict(try_test))))[0])
                p3=1-p_covid if p_covid<0.5 else p_covid
                p3=round(p3*100,4)
                p3=100-p3 if p3<50 else p3

                prediction_covid_pred='COVID' if prediction_covid<0.5 else 'NORMAL' 
                pred.append(prediction_covid_pred)
                print(p1,p2,p3)


                if ('TUBERCULOSIS' in pred) or ('PNEUMONIA' in pred) or ('COVID' in pred):
                    if 'COVID' in pred:
                        print('TUBERCULOSIS')

                        
                        b=text=str(p1)+"% POSITIVE"

                    else:


                        
                        b=text=str(p1)+"% NEGATIVE"


                    if 'PNEUMONIA' in pred:
                        print('PNEUMONIA')
                        
                        c=text=str(p2)+"% POSITIVE"
                    else:

                        
                        c=text=str(p2)+"% NEGATIVE"

                    if 'TUBERCULOSIS' in pred:
                        print('COVID-19')
                        
                        d=text=str(p3)+"% POSITIVE"
                    else:

                        
                        d=text=str(p3)+"% NEGATIVE"
                else:
                    print('NORMAL')

                    b=text=str(p1)+"% NEGATIVE"
                    c=text=str(p2)+"% NEGATIVE"
                    d=text=str(p3)+"% NEGATIVE"

            

            return render_template("index.html",a=a,b=b,c=c,d=d,path=filepath)
             
    return render_template("index.html")

if __name__=='__main__':
    app.secret_key='abc'
    app.run(debug=True)
