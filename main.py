from flask import Flask, render_template 
from flask import request
from flask import jsonify
import pymysql

# Flask 앱 인스턴스 생성
app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_name = data['USER_NAME']
    user_id = data['EMAIL']
    user_pw = data['PASSWORD']
    
    if validation_name(user_name) and validation_id(user_id) and validation_pw(user_pw):
        connection = pymysql.connect(host='localhost', port='8080', db='storagelocker', user='root', pw='1807992102', charset='utf8')
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = " "
        
        connection.commit()
        connection.close()

        return jsonify({'message':'회원가입 완료'})

def validation_name(name):
    if len(name) > 0 and len(name) < 20:
        return True
    else:
        return False

def validation_id(id):
    return 1

def validation_pw(pw):
    return 0

# 로그인 엔드포인트 정의, POST 메소드로 설정
@app.route('/login', method = ['POST'])
def login():
    # MySQL 데이터베이스 연결
    connection = pymysql.connect(host='localhost', port='8080', db='storagelocker', user='root', pw='1807992102', charset='utf8')
    # 데이터에 접근
    cursor = connection.cursor(pymysql.cursors.Dict)

    data = request.get_json()
    user_id = data['EMAIL']
    user_pw = data['PASSWORD']

    # SQL query 작성
    sql = "SELECT * FROM USER_LOGIN WHERE EMAIL = %s"

    # SQL query 실행
    cursor.execute(sql, (user_id, ))
    # DB 데이터 가져오기
    db_data = cursor.fetchall()

    # Database 닫기
    connection.close()
    
    # 데이터베이스에서 사용자 정보를 가져왔는지 확인
    if len(db_data) > 0:
        db_name = db_data[0]['USER_NAME']
        db_id = db_data[0]['EMAIL']
        db_pw = db_data[0]['PASSWORD']

        return jsonify({'message':'로그인이 완료 되었습니다.'})
    else:
        return jsonify({'message':'로그인 정보를 다시 입력해주세요.'})
    
if __name__ == '__main__':
    app.run(debug=True, host = 'localhost', port = 8080)