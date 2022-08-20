chain = []

block1 = {
    'type': 'open',                                         # 투표 타입 - 열림 (open)
    'data': {                                               # 투표에 관한 정보들
        'id': '투표 ID',
        'question': '투표 질문',
        'options': ['투표 항목1', '투표 항목2', '투표 항목3']
    }
}

chain.append(block1)

block2 = {
    'type': 'vote',                 # 타입 - 투표
    'data': {                       # 투표 정보 - ('어디에', '무엇을')
        'id': '투표 ID',
        'vote': '투표 항목1'
    }
}

chain.append(block2)
print(chain)