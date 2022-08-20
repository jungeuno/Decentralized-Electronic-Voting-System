from flask import Flask
app = Flask(__name__)           # 웹 페이지 연결

@app.route("/")                 # 기본 경로
def f1():
    return "시작 페이지"

@app.route('/a')                # () 안의 문자를 경로에 추가하면 보여지는 페이지
def f2():
    return 'a'

app.run()
