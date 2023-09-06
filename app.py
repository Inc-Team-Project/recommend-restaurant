from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, REST_INFO, REST_MENU, REST_REVIEW  # 모델 import

app = Flask(__name__)

# SQLAlchemy 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@172.20.132.178:4406/restaurant'
db.init_app(app)

@app.route('/')
def index():
    # REST_INFO, REST_MENU, REST_REVIEW 테이블에서 데이터를 조회하여 index.html 템플릿에 전달
    rest_info_data = REST_INFO.query.all()
    rest_menu_data = REST_MENU.query.all()
    rest_review_data = REST_REVIEW.query.all()
    return render_template('index.html', rest_info_data=rest_info_data, rest_menu_data=rest_menu_data, rest_review_data=rest_review_data)

@app.route('/add')
def add():
    # REST_INFO, REST_MENU, REST_REVIEW 테이블에서 데이터를 조회하여 add.html 템플릿에 전달
    rest_info_data = REST_INFO.query.all()
    rest_menu_data = REST_MENU.query.all()
    rest_review_data = REST_REVIEW.query.all()
    return render_template('add.html', rest_info_data=rest_info_data, rest_menu_data=rest_menu_data, rest_review_data=rest_review_data)

@app.route('/detail/<rest_name>')
def detail(rest_name):
    # REST_INFO 테이블에서 특정 레스토랑의 정보를 조회하고, REST_MENU 테이블에서 해당 레스토랑의 메뉴 정보를 조회하여 detail.html 템플릿에 전달
    rest_info_data = REST_INFO.query.filter_by(REST_Name=rest_name).first()
    rest_menu_data = REST_MENU.query.filter_by(REST_Name=rest_name).all()
    rest_review_data = REST_REVIEW.query.all()
    return render_template('detail.html', rest_info_data=rest_info_data, rest_menu_data=rest_menu_data,rest_review_data=rest_review_data)

@app.route('/add', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # 폼에서 입력한 데이터를 받아와 데이터베이스에 추가하고, 인덱스 페이지로 리다이렉트
        REST_Name = request.form['REST_Name']
        REST_Type = request.form['REST_Type']
        REST_Address = request.form['REST_Address']
        REST_Web = request.form['REST_Web']
        Tel = request.form['Tel']
        MENU_Name = request.form['MENU_Name']
        MENU_Price = request.form['MENU_Price']

        # 데이터베이스에 데이터 추가
        rest_info = REST_INFO(REST_Name=REST_Name, REST_Type=REST_Type, REST_Address=REST_Address, REST_Web=REST_Web, Tel=Tel)
        db.session.add(rest_info)

        rest_menu = REST_MENU(REST_Name=REST_Name, MENU_Name=MENU_Name, MENU_Price=MENU_Price)
        db.session.add(rest_menu)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit_review/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    if request.method == 'POST':
        # review_id를 사용하여 해당 댓글을 가져온다.
        review = REST_REVIEW.query.get(review_id)
        
        if review:
            # 댓글의 내용을 수정한다.
            review.R_Score = request.form['R_Score']
            review.R_Text = request.form['R_Text']
            
            # 수정한 내용을 저장한다.
            db.session.commit()
            return redirect(url_for('detail', rest_name=review.REST_Name))
    
    return 'Review not found', 404

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    try:
        # 클라이언트에서 전송한 JSON 데이터에서 비밀번호를 받아옵니다.
        data = request.get_json()
        password = data.get('password')

        # 비밀번호가 '1234'가 아닌 경우 삭제를 거부합니다.
        if password != '1234':
            return 'Invalid password', 403  # 403 Forbidden 상태 코드 반환

        # 댓글 ID를 사용하여 댓글을 조회하고 삭제합니다.
        review = REST_REVIEW.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return '', 204  # 성공적인 삭제를 나타내는 204 상태 코드 반환
        else:
            return 'Review not found', 404
    except Exception as e:
        return str(e), 500  # 오류가 발생한 경우 500 Internal Server Error 상태 코드 반환
    
@app.route('/list', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']

        # 검색 조건을 적용하여 데이터베이스에서 데이터를 검색하고, 검색 결과를 list.html 템플릿에 전달
        results = REST_INFO.query.filter(
            (REST_INFO.REST_Name.contains(query)) |
            (REST_INFO.REST_Type.contains(query)) |
            (REST_INFO.REST_Address.contains(query))
        ).all()

        return render_template('list.html', results=results)

    return render_template('list.html')

@app.route('/go/<path:web_address>')
def go(web_address):
    # web_address에 해당하는 URL로 리다이렉트
    return redirect(web_address)

# Flask 앱의 댓글 관련 라우트
@app.route('/add_review/<string:rest_name>', methods=['POST'])
def add_review(rest_name):
    
    if request.method == 'POST':
        R_Score = request.form['R_Score']
        R_Text = request.form['R_Text']

        # REST_REVIEW 테이블에 데이터 추가
        review = REST_REVIEW(REST_Name=rest_name, R_Score=R_Score, R_Text=R_Text)
        db.session.add(review)
        db.session.commit()
    return redirect(url_for('detail', rest_name=rest_name))

@app.route('/list/<type>')
def list_by_type(type):
    # type에 해당하는 음식점을 데이터베이스에서 검색하고, list.html 템플릿에 전달
    restaurants = REST_INFO.query.filter_by(REST_Type=type).all()
    return render_template('list.html', results=restaurants)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
