# file name : test.py
# pwd : /ISIA_coffee/app/test/test.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

from random import *
import os
import testremove
import supervised_IAFC

from app.module import dbModule

test = Blueprint('test', __name__, url_prefix='/test')

file = 'C:/ProgramData/MySQL/MySQL Server 8.0/Data/isiadb/coffee.csv'

@test.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')

# INSERT 함수 예제
@test.route('/insert', methods=['GET'])
def insert():
    db_class = dbModule.Database()

    randomDensity = randint(1, 10)
    if randomDensity <= 5:
        target = 1
    elif randomDensity >= 6:
        target = 2
    print("Density :", randomDensity, "Target :", target)

    sql = "INSERT INTO ISIADB.coffee(density, target) \
           VALUES('%d', '%d')" % (randomDensity, target) #이 곳에다가 진하기 1~10, target저장
    db_class.execute(sql)
    db_class.commit()

    sql = "SELECT COUNT(*) FROM coffee"
    row_count = db_class.CustomexecuteAll(sql)
    print("Count :", row_count)

    return render_template('/main/index.html',
                           result='insert is done!',
                           densityData=None,
                           countData=row_count)

# SELECT 함수 예제
@test.route('/select', methods=['GET'])
def select():
    db_class = dbModule.Database()

    sql = "SELECT density, target \
           FROM ISIADB.coffee"
    row = db_class.executeAll(sql)
    print(row)

    return render_template('/main/index.html',
                           result=None,
                           densityData=row[0])

# UPDATE 함수 예제
@test.route('/export', methods=['GET'])
def update():
    db_class = dbModule.Database()

    if os.path.isfile(file):
        return render_template('/main/index.html',
                               check="already file exist",
                               result=None,
                               densityData=None)
    else:
        sql = "SELECT * FROM coffee INTO OUTFILE 'coffee.csv' CHARACTER SET utf8 FIELDS TERMINATED BY ','"

        db_class.execute(sql)
        db_class.commit()

        return render_template('/main/index.html',
                               check="create success",
                               result=None,
                               densityData=None)

@test.route('/remove', methods=['GET'])
def remove():
    if os.path.isfile(file):
        testremove.remove()
        return render_template('/main/index.html',
                               check="remove success",
                               result=None,
                               densityData=None)
    else:
        return render_template('/main/index.html',
                               check="file not exist",
                               result=None,
                               densityData=None)

@test.route('/learning', methods=['GET'])
def learning():
    db_class = dbModule.Database()
    class1, class2 = supervised_IAFC.learning()

    sql = "DELETE FROM centroid"
    db_class.execute(sql)
    db_class.commit()

    sql = "INSERT INTO ISIADB.centroid(centroid_1, centroid_2) \
               VALUES('%c', '%c')" % (class1, class2)
    db_class.execute(sql)
    db_class.commit()

    return render_template('/main/index.html',
                           result=None,
                           densityData=None,
                           class1 = class1,
                           class2 = class2)

@test.route('/result', methods=['GET'])
def result():
    db_class = dbModule.Database()

    sql = "SELECT centroid_1, centroid_2 \
               FROM ISIADB.centroid"
    row = db_class.CustomexecuteOne(sql)
    centroid_1 = int(row['centroid_1'])
    centroid_2 = int(row['centroid_2'])

    return render_template('/main/index.html',
                           result=None,
                           densityData=None,
                           centroid_1=centroid_1,
                           centroid_2=centroid_2)

@test.route('/dataremove', methods=['GET'])
def dataremove():
    db_class = dbModule.Database()

    sql = "DELETE FROM coffee"
    db_class.execute(sql)
    db_class.commit()

    return render_template('/main/index.html')

"""
@test.route('/export', methods=['GET'])
def update():
    db_class = dbModule.Database()

    sql = "UPDATE ISIADB.coffee \
           SET density = '%d' \
           WHERE density = 110" % (110110)
    db_class.execute(sql)
    db_class.commit()

    sql = "SELECT density, target \
           FROM ISIADB.coffee"
    row = db_class.executeAll(sql)

    return render_template('/main/index.html',
                           result=None,
                           densityData=row[0])
"""