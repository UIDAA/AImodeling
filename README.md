# 신용카드 대금 연체 예측

카드사 채무 상담팀이 한 달에 먼저 연락할 수 있는 고객(전체의 상위 5%)을 고르는 모델을 만든다.
1순위 지표는 Precision@5% 이다. 자세한 규칙은 [CLAUDE.md](CLAUDE.md) 참고.

## 실행 방법

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 데이터 받기 (UCI, 약 5MB)
mkdir -p data/raw
curl -L -o data/raw/credit_default.zip "https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip"
unzip -o data/raw/credit_default.zip -d data/raw

# 1차시: 데이터 첫 관찰 (data/credit_default.csv 생성)
python src/01_first_look.py

# 2차시: 분할 → 탐색 그래프 → 전처리 확인
python src/02_split.py
python src/03_eda.py
python src/preprocess.py
```

## 폴더 구조

- `data/` 데이터 (깃허브에 올리지 않음, 위 명령으로 받음)
- `src/` 코드 (차시 순서대로 번호를 붙임)
- `figures/` 그래프
- `data_card.md` 데이터 카드
- `ai_log.md` AI 활용 기록
- `scoreboard.csv` 모델 순위표 (3차시부터)
