from flask import Flask, jsonify, request                  # jsonify - json 형식으로 변환해줌
app = Flask(__name__)

@app.route('/api1', methods=['GET'])                       # 기본값은 Get 방식
def f1():
    return jsonify({'status': 'success'})                  # 쌍따옴표로 변환되어 확인됨


@app.route('/api2', methods=['POST'])                      # POST 방식
def f2():
    data = request.get.json()
    return jsonify(data)


app.run()