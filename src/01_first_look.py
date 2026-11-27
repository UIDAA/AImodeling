"""1차시: 데이터 첫 관찰
- 원본 엑셀(.xls)을 읽어서 csv 로 저장한다
- 크기(행·열), 열 이름, 정답 비율, 결측, 중복, 이상한 범주 값을 확인한다
- 아직 Train/Valid/Test 로 나누지 않는다 (2차시에 함)
"""
import pandas as pd

RAW = 'data/raw/default of credit card clients.xls'

# 엑셀 첫 줄은 X1, X2... 같은 기호, 두 번째 줄이 진짜 열 이름 → header=1
df = pd.read_excel(RAW, header=1)
df = df.rename(columns={'default payment next month': 'default'})
df.to_csv('data/credit_default.csv', index=False)

print('1) 크기:', df.shape[0], '행 ×', df.shape[1], '열')
print('2) 열 이름:', list(df.columns))

n_pos = int(df['default'].sum())
print(f'3) 정답(연체) 비율: {n_pos}명 / {len(df)}명 = {df["default"].mean():.4f}')

print('4) 결측 칸 수 합계:', int(df.isna().sum().sum()))
print('5) 완전히 같은 행(ID 제외):', int(df.drop(columns='ID').duplicated().sum()))
print('   ID 중복:', int(df['ID'].duplicated().sum()))

print('6) 범주형 열 값 분포 (설명서 정의: SEX 1·2 / EDUCATION 1~4 / MARRIAGE 1~3)')
for col in ['SEX', 'EDUCATION', 'MARRIAGE']:
    print(f'   {col}:', df[col].value_counts().sort_index().to_dict())

print('7) 상환 상태 PAY_* 값 종류 (설명서 정의: -1 제때 납부, 1~9 연체 개월 수)')
for col in ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']:
    print(f'   {col}:', sorted(df[col].unique().tolist()))

bill = [f'BILL_AMT{i}' for i in range(1, 7)]
print('8) 청구액이 음수인 칸 수:', int((df[bill] < 0).sum().sum()))
print('9) 숫자 열 요약')
print(df[['LIMIT_BAL', 'AGE', 'BILL_AMT1', 'PAY_AMT1']].describe().round(0).to_string())
