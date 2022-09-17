import requests                                 # get / post 방식
import json

while True:
    print('1. 블록 체인 조회')
    print('2. 투표 생성')
    print('3. 투표')
    print('4. 종료')

    menu = input('=> ')                         # 메뉴 선택지를 입력받음

    if menu == '1':                             # 블록 체인 조회 기능 (./lab_client/01. list)
        res = requests.get('http://127.0.0.1:5000/list')
        print(res.text)
    elif menu == '2':                           # 투표 생성 기능 (./lab_client/02. open)
        headers = {'Content-Type': 'application/json'}

        question = input('질문: ')                                # 투표 질문
        option1 = input('선택지1: ')                              # 투표 선택지
        option2 = input('선택지2: ')
        option3 = input('선택지3: ')

        data = {
            'question': question,                                # 투표 질문
            'options': [option1, option2, option3]               # 투표 선택지
        }

        res = requests.post(
            'http://127.0.0.1:5000/open',
            data=json.dumps(data),                               # json.dumps(data) - data 객체를 JSON 문자열로 변환
            headers=headers)
        print(res.text)
    elif menu == '3':                                            # 투표 기능 (./lab_client/ 03. vote)
        headers = {'Content-Type': 'application/json'}

        id = input('투표 아이디')
        vote = input('투표 항목')

        data = {'id': id, 'vote': vote}

        res = requests.post(
            'http://127.0.0.1:5000/vote',
            data=json.dumps(data),
            headers=headers)
        print(res.text)
    elif menu == '4':                                            # 종료 기능
        break


