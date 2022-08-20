from flask import Flask
app = Flask(__name__)

@app.route('/api1', methods=['GET'])                       # 기본값은 Get 방식
def f1():
    return 'GET api1'





@app.route('/api2', methods=['POST'])
def f2():
    return 'POST api2'



app.run()