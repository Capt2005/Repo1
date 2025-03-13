from flask import Flask
from flask import *
from flask_restful import Resource,Api
import pymysql
import pymysql.cursors

app = Flask(__name__)
api = Api(app)
class Farmer(Resource):

    def get(self):
        connection = pymysql.connect(host='CaptHM.mysql.pythonanywhere-services.com', user='CaptHM', password='@2005HM@',database='CaptHM$default')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "select * from farmer"
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return jsonify({'message':'NO FOUND RECORDS'})
        else:
            farmer = cursor.fetchall()
            return jsonify(farmer)

    def post(self):
        data = request.json
        farmer_id = data['farmer_id']
        farmer_name = ['farmer_name']
        farmer_location=['farmer_location']
        earnings = ['earnings']

        connection = pymysql.connect(host='CaptHM.mysql.pythonanywhere-services.com', user='CaptHM', password='@2005HM@',database='CaptHM$default')
        cursor = connection.cursor()
        sql = '''
            insert into farmer(farmer_id, farmer_name,farmer_location,earnings)
            values(%s,%s,%s,%s)
        '''
        try:
            cursor.execute,(sql,(farmer_id, farmer_name,farmer_location,earnings))
            connection.commit()
            return jsonify({'message':'RECORD SAVED'})
        except:
            connection.rollback()
            return jsonify({'message':'RECORD NOT SAVED'})

    def delete(self):
        data = request.json
        farmer_id = data['farmer_id']
        connection = pymysql.connect(host='CaptHM.mysql.pythonanywhere-services.com', user='CaptHM', password='@2005HM@',database='CaptHM$default')
        cursor = connection.cursor()
        sql = "delete from farmer where farmer_id = %s"
        try:
            cursor.execute(sql, farmer_id)
            connection.commit()
            return jsonify({'message':"DELETED SUCCESSFULLY"})
        except:
            connection.rollback()
            return jsonify({'message':"DELETION FAILED"})

    def put(self):
        data = request.json
        farmer_id = data['farmer_id']
        earnings = data['earnings']
        connection = pymysql.connect(host='CaptHM.mysql.pythonanywhere-services.com', user='CaptHM', password='@2005HM@',database='CaptHM$default')
        cursor = connection.cursor()
        sql = "update farmer SET earnings = %s where farmer_id = %s"
        try:
            cursor.execute(sql,(earnings, farmer_id))
            connection.commit()
            return jsonify({'message':"UPDATED SUCCESSFULLY"})
        except:
            connection.rollback()
            return jsonify({'message':"UPDATE FAILED"})

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == "POST":
        data = request.json
        username = data['username']
        email = data['email']
        phone = data['phone']
        password1 = data['password1']
        password2 = data['password2']

        if password1.length() < 7:
            return jsonify({'message':'password should be at least 8 characters'})
        elif password1 != password2:
            return jsonify({'message':'passwords do not match'})
    else:
        connection = pymysql.connect(host='CaptHM.mysql.pythonanywhere-services.com', user='CaptHM', password='@2005HM@',database='CaptHM$default')
        cursor = connection.cursor()
        sql = '''
            insert into users(username, email,phone,password)
            values(%s,%s,%s,%s)
        '''
        try:
            cursor.execute,(sql,(username, email,phone,password1))
            connection.commit()
            return jsonify({'message':'Registration successful'})
        except:
            connection.rollback()
            return jsonify({'message':'Registration failed'})

#else:
    #   pass

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == "POST":
        data = request.json
        username = data['username']
        password = data['password']

        connection = pymysql.connect(host='CaptHM.mysql.pythonanywhere-services.com', user='CaptHM', password='@2005HM@',database='CaptHM$default')
        cursor = connection.cursor(pymysql.cursor.Dictcursor)

        sql = "select * from users where username = %s and password = %s"
        try:
            cursor.execute,(sql,(username, password))

            if cursor.rowcount() == 0:
                return jsonify({'message':'Invalid credentials', 'user':'Null'})
            else:
                user = cursor.fetchone()
                return jsonify({'message':'login successful', 'user':'user'})
        except:
            return jsonify({'message':'Error occured', 'user':'Null'})
    else:
        pass


api.add_resource(Farmer,'/farmer')
if __name__ == '__main__':
    app.run()
