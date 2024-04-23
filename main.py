from flask import Flask, render_template 
from flask import request
from flask import jsonify
import pymysql

# Flask 앱 인스턴스 생성
app = Flask(__name__)

# 홈 페이지 기능
@app.route('/home', methods=['GET','POST'])
def home():
    connection = pymysql.connect(host='localhost', port='8080', db='storagelocker', user='root', pw='1807992102', charset='utf8')
    conn = connection.cursor(pymysql.cursors.DictCursor)
    sql = "select * from user_storage where ... "
    conn.execute(sql)
    result = conn.fetchall()
    return "미정" # 임시 반환 값

# 로그인 페이지 기능
@app.route('/log')
def log():
    return 1

# 마이페이지 기능
@app.route('/my_page')
def mypage():
    return 2

# 보관함 정보에 대한 기능
@app.route('/info')
def info():
    return 3

# 회원가입 기능, POST 메소드로 설정
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_name = data['USER_NAME']
    user_id = data['EMAIL']
    user_pw = data['PASSWORD']
    
    if validation_name(user_name) and validation_id(user_id) and email_overlap(user_id) and validation_pw(user_pw):
        connection = pymysql.connect(host='localhost', port='8080', db='storagelocker', user='root', pw='1807992102', charset='utf8')
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = ""
        
        connection.commit()
        connection.close()

        return jsonify({'message':'회원가입이 완료되었습니다.'})

    elif validation_id(user_id) or validation_pw(user_pw):
        return jsonify({'message':'아이디 또는 비밀번호를 양식에 맞게 작성해 주세요'})
    elif email_overlap(user_id) == False:
        return jsonify({'message':'이미 사용 중인 이메일 주소입니다.'})
    elif validation_name(user_name) == False:
        return jsonify({'message':'올바른 이름을 입력해주세요'})
    else:
        return jsonify({'message':'잘못된 입력입니다.'})


# 유저 이름 형식 확인
def validation_name(name):
    if len(name) > 0 and len(name) < 20:
        return True
    else:
        return False

# 유저 아이디 형식 확인
def validation_id(id):
    if '@' in id and id > 0 and id < 30:
        return True
    else:
        return False

# 유저 아이디 중복 확인
def email_overlap(email):
    connection = pymysql.connect(host='localhost', port=8080, db='storagelocker', user='root', password='1807992102', charser='utf8')
    cursor = connection.cursor(pymysql.cusors.DictCursor)

    sql = "SELECT * USER_LOGIN WHERE EMAIL = %s"
    cursor.execute(sql, (email,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return False
    else:
        return True

# 유저 비밀번호 형식 확인
def validation_pw(pw):
    if pw > 8 and pw < 30:
        return True
    else:
        return False

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

        return jsonify({'message':f'{db_name}님 로그인이 완료 되었습니다.'})
    else:
        return jsonify({'message':'로그인 정보를 다시 입력해주세요.'})
    
if __name__ == '__main__':
    app.run(debug=True, host = 'localhost', port = 8080)