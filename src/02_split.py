"""2차시: Train / Valid / Test 분할
- 6:2:2 로 나눈다. 한 번에 못 나누니까 6:4 로 자른 뒤 4 를 반으로 다시 자른다
- stratify 로 세 조각의 연체 비율을 똑같이 맞춘다
- 중복 행(ID 만 다른 행)은 다른 사람으로 보고 그대로 둔다 (ai_log 참고)
"""
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('data/credit_default.csv')

train, temp = train_test_split(df, test_size=0.4, stratify=df['default'], random_state=42)
valid, test = train_test_split(temp, test_size=0.5, stratify=temp['default'], random_state=42)

for name, part in [('train', train), ('valid', valid), ('test', test)]:
    part.to_csv(f'data/{name}.csv', index=False)
    print(f'{name:6s} {len(part):5d}행  연체 {int(part["default"].sum()):4d}명  {part["default"].mean():.4f}')

# 세 조각에 같은 고객(ID)이 겹치지 않는지 확인
ids = [set(p['ID']) for p in (train, valid, test)]
print('조각 사이에 겹치는 ID 수:', len(ids[0] & ids[1]) + len(ids[0] & ids[2]) + len(ids[1] & ids[2]))
