import sqlite3
import os
import random
import configparser

pwd = ""
cf = configparser.ConfigParser()
def load():
    cf.read('./app.conf')
    cf.sections()
    pwd=cf['APPLICATION']['ApplicationDirectory']
    db=sqlite3.connect(os.path.join(pwd,"data/data.sqlite3"))
    db_exec=db.cursor()
    db_exec.execute("DELETE FROM blessings")
    for (root,dirs,files) in os.walk(os.path.join(pwd,"static"), topdown=True):
        if files != []:
            lang = os.path.basename(root)
            for f in files:
                fpath = os.path.join(root, f)
                rel_fpath = os.path.relpath(fpath, pwd)
                param=(lang, rel_fpath)
                db_exec.execute("INSERT INTO blessings VALUES (NULL, ?, ?)", param)
    db.commit()
    db.close()

def pick_random(lang):
    db=sqlite3.connect(os.path.join(pwd,"data/data.sqlite3"))
    db_exec=db.cursor()
    all = db_exec.execute("SELECT * FROM blessings WHERE language = '{}'".format(lang))
    arr=all.fetchall()
    return random.choice(arr)[2]

def pick_this(lang, img):
    db=sqlite3.connect(os.path.join(pwd, "data/data.sqlite3"))
    db_exec=db.cursor()
    all = db_exec.execute("SELECT * FROM blessings WHERE language = '{}'".format(lang))
    arr=all.fetchall()
    im=os.path.basename(img)
    im="/"+im
    for i in arr:
        if im in i[2]:
            return i[2]
    return pick_random(lang)
