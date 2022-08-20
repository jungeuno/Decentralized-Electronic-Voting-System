from flask import Flask, jsonify, request
app = Flask(__name__)

chain = []
cnt = 0                                 # 오픈된 투표 수 - 중복 방지

@app.route('/list', methods=['GET'])
def vote_list():
    return jsonify(chain)

@app.route('/open', methods=['POST'])
def vote_open():
    global cnt
    try:                                # 코드 실행 중 에러 발생하더라도 실행하도록
        data = request.get_json()
        block = {
            'type': 'open',
            'data': {
                'id': str(cnt),
                'question': data['question'],
                'options': data['options']
            }
        }
        cnt += 1                        # 중복 방지
        chain.append(block)
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'fail'})

@app.route('/vote', methods=['POST'])
def vote():
    try:
        data = request.get_json()
        block = {
            'type': 'vote',
            'data': {
                'id': data['id'],
                'vote': data['vote']
            }
        }
        data.append(block)
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'fail'})

app.run()