# file name : dbModule.py
# pwd : /ISIA_coffee/app/module/dbModule.py
import json
import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user = 'root',
                                  password = 'wogml231!',
                                  db = 'ISIADB',
                                  charset = 'utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def CustomexecuteAll(self, query, args={}):
        self.cursor.execute(query, args)
        
        # fetch로 받은 데이터 [{"COUNT(*)": 109}]를 json으로 변환
        # -> key : value로 변환하여 값만 가져오기 위함
        # 즉 인코딩 작업
        row = json.dumps(self.cursor.fetchall())
        # json 디코딩 (type : list)
        row_decode = json.loads(row)
        # list의 첫 번째 row에서 COUNT(*)라는 key의 value를 가져오기 위함
        return row_decode[0]['COUNT(*)']

    def CustomexecuteOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = json.dumps(self.cursor.fetchone())
        row_decode = json.loads(row)
        return row_decode

    def commit(self):
        self.db.commit()