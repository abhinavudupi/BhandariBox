from flask import Flask, render_template, request, redirect
import os
from gpiozero import LED, DigitalInputDevice, Button
import sqlite3
from application import load_blessings

contrib_flag=False
btn1_flag=False
btn2_flag=False
btn3_flag=False

app = Flask(__name__)
load_blessings.load()

def contributed():
    global contrib_flag
    contrib_flag=True
def pressed1():
    global btn1_flag
    btn1_flag=True
def pressed2():
    global btn2_flag
    btn2_flag=True
def pressed3():
    global btn3_flag
    btn3_flag=True

led1=LED(4)
led2=LED(24)
sensor=DigitalInputDevice(15)
button1=Button(17)
button2=Button(18)
button3=Button(27)

sensor.when_activated = contributed
button1.when_pressed = pressed1
button2.when_pressed = pressed2
button3.when_pressed = pressed3

@app.route('/')
def home():
    global contrib_flag
    global btn1_flag
    global btn2_flag
    global btn3_flag
    led1.off()
    btn1_flag=False
    btn2_flag=False
    btn3_flag=False
    contrib_flag=False
    return render_template('index.html')

@app.route('/api/check/contribution')
def check_contrib():
    global contrib_flag
    global btn1_flag
    global btn2_flag
    global btn3_flag
    if contrib_flag==True:
        btn1_flag=False
        btn2_flag=False
        btn3_flag=False
        contrib_flag=False
        return "1"
    else:
        return "0"
    
@app.route('/api/check/button')
def check():
    global btn1_flag
    global btn2_flag
    global btn3_flag
    if btn1_flag==True:
        btn1_flag=False
        btn2_flag=False
        btn3_flag=False
        return "2"
    elif btn2_flag==True:
        btn1_flag=False
        btn2_flag=False
        btn3_flag=False
        return "3"
    elif btn3_flag==True:
        btn1_flag=False
        btn2_flag=False
        btn3_flag=False
        return "4"
    else:
        return "0"

@app.route('/bless/<language>')
def about(language):
    led1.on()
    try:
        im = request.args.get("curimg")
        if (im == None) or (im==""):
            raise Exception("first blessing")
        path=load_blessings.pick_this(language, im)
    except:
        path=load_blessings.pick_random(language)
    finally:
        return render_template('bless.html', lang=language, imgpath="/"+path)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8080)
