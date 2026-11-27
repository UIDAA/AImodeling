"""2차시: 전처리 규칙 (3차시부터 모든 모델이 이 파일을 불러서 씀)

내가 정한 규칙 (ai_log.md 참고)
1. 중복 행(ID 만 다른 행)은 다른 사람으로 보고 그대로 둔다      → 02_split.py 에서 처리 안 함
2. EDUCATION 0·5·6 → 4(기타), MARRIAGE 0 → 3(기타) 로 합친다     → clean()
3. PAY_0 ~ PAY_6 은 숫자 그대로 쓴다 (-2 ~ 8, 클수록 더 늦게 냄)
4. 금액 열(한도·청구액·납부액)은 RobustScaler 로 크기를 맞춘다

기준값(중앙값, IQR, 평균, 표준편차, 범주 목록)은 Pipeline 의 fit 이 Train 에서만 구한다.
"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, RobustScaler, StandardScaler

TARGET = 'default'

MONEY = ['LIMIT_BAL'] + [f'BILL_AMT{i}' for i in range(1, 7)] + [f'PAY_AMT{i}' for i in range(1, 7)]
PAY = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
OTHER_NUM = ['AGE']
CAT = ['SEX', 'EDUCATION', 'MARRIAGE']
FEATURES = MONEY + PAY + OTHER_NUM + CAT          # ID 와 정답 열은 넣지 않음


def clean(df):
    """정의 밖 범주를 '기타'로 합친다.
    데이터에서 무언가를 배우지 않는 고정 규칙이라 Train·Valid·Test 에 똑같이 써도 누수가 없다."""
    df = df.copy()
    df['EDUCATION'] = df['EDUCATION'].replace({0: 4, 5: 4, 6: 4})
    df['MARRIAGE'] = df['MARRIAGE'].replace({0: 3})
    return df


def load(name):
    """data/{name}.csv 를 읽고 clean() 을 거쳐 X(입력), y(정답) 로 돌려준다.
    name='test' 는 최종 판정 때만 쓴다 (CLAUDE.md 규칙)."""
    df = clean(pd.read_csv(f'data/{name}.csv'))
    return df[FEATURES], df[TARGET]


def build_preprocessor():
    """모델 앞에 붙일 전처리 묶음. 사용 예:
    Pipeline([('pre', build_preprocessor()), ('clf', LogisticRegression())])"""
    return ColumnTransformer([
        ('money', RobustScaler(), MONEY),
        ('num', StandardScaler(), PAY + OTHER_NUM),
        ('cat', OneHotEncoder(handle_unknown='ignore'), CAT),
    ])


if __name__ == '__main__':
    # 확인용: 기준값이 정말 Train 에서만 나왔는지 눈으로 본다
    X_train, y_train = load('train')
    X_valid, y_valid = load('valid')

    pre = build_preprocessor().fit(X_train)       # Train 으로만 fit
    rs = pre.named_transformers_['money']

    print('[확인 1] RobustScaler 가 배운 중앙값 vs 직접 계산한 중앙값 (앞 3개 열)')
    for i, col in enumerate(MONEY[:3]):
        print(f'  {col:10s} 배운 값 {rs.center_[i]:>10,.0f}  Train {X_train[col].median():>10,.0f}'
              f'  Valid {X_valid[col].median():>10,.0f}')

    print('[확인 2] clean() 뒤 범주 값 (Train)')
    for col in ['EDUCATION', 'MARRIAGE']:
        print(f'  {col}:', X_train[col].value_counts().sort_index().to_dict())

    Xt = pre.transform(X_valid)
    print('[확인 3] 변환 뒤 Valid 크기:', Xt.shape, '(원-핫 때문에 열이 늘어남)')
    print('[확인 4] 입력 열에 정답·ID 가 없는지:', TARGET not in FEATURES and 'ID' not in FEATURES)
