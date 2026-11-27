"""2차시: 탐색 그래프 2개 (train.csv 만 사용)
- 그림 1: 가장 최근 달 상환 상태(PAY_0) 값별 연체 비율
- 그림 2: 카드 한도(LIMIT_BAL) 구간별 연체 비율
- valid.csv, test.csv 는 읽지 않는다
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

# 한글 글꼴: 맥 / 윈도 / 리눅스 순서로 있는 것을 씀
plt.rcParams['font.family'] = ['AppleGothic', 'Malgun Gothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BLUE = '#2a78d6'      # 막대 색 (한 가지 색만 씀)
INK = '#52514e'       # 글자·기준선 색
GRID = '#e4e3df'

train = pd.read_csv('data/train.csv')
overall = train['default'].mean()


def bar_rate(ax, labels, rates, counts, title, xlabel, ymax=100):
    """구간별 연체 비율 막대 + 전체 평균 점선"""
    ax.bar(range(len(labels)), rates * 100, color=BLUE, width=0.7)
    ax.axhline(overall * 100, color=INK, linestyle='--', linewidth=1, label=f'전체 평균 {overall:.1%}')
    ax.legend(loc='upper left', frameon=False, fontsize=9)
    for i, (r, n) in enumerate(zip(rates, counts)):
        ax.text(i, r * 100 + 1, f'{r:.0%}\n({n:,}명)', ha='center', va='bottom', fontsize=8, color=INK,
                bbox=dict(facecolor='white', edgecolor='none', pad=1))
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, ymax)
    ax.set_ylabel('연체 비율 (%)')
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc='left', fontsize=12)
    ax.grid(axis='y', color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)


# ── 그림 1: PAY_0 값별 연체 비율 ──
# 3 이상은 인원이 적어서 '3+' 로 묶음
pay0 = train['PAY_0'].clip(upper=3)
g = train.groupby(pay0)['default'].agg(['mean', 'size'])
labels = ['-2\n사용 없음', '-1\n전액 납부', '0\n최소 납부', '1\n1달 연체', '2\n2달 연체', '3+\n3달 이상']
fig, ax = plt.subplots(figsize=(8, 4.5))
bar_rate(ax, labels, g['mean'].values, g['size'].values,
         '그림 1. 지난달(9월) 상환 상태별 다음 달 연체 비율 (Train 18,000명)', 'PAY_0 값')
fig.tight_layout()
fig.savefig('figures/fig1_pay0_default_rate.png', dpi=150)
print('그림 1 저장. PAY_0 값별 연체 비율:')
print(g.round(3).to_string())

# ── 그림 2: 한도 구간별 연체 비율 ──
edges = [0, 50_000, 100_000, 200_000, 300_000, 500_000, 1_000_001]
names = ['5만 이하', '5~10만', '10~20만', '20~30만', '30~50만', '50만 초과']
lim = pd.cut(train['LIMIT_BAL'], bins=edges, labels=names, right=True)
g2 = train.groupby(lim, observed=False)['default'].agg(['mean', 'size'])
fig, ax = plt.subplots(figsize=(8, 4.5))
bar_rate(ax, names, g2['mean'].values, g2['size'].values,
         '그림 2. 카드 한도 구간별 연체 비율 (Train 18,000명, 단위: 대만달러)', 'LIMIT_BAL 구간', ymax=50)
fig.tight_layout()
fig.savefig('figures/fig2_limit_default_rate.png', dpi=150)
print('\n그림 2 저장. 한도 구간별 연체 비율:')
print(g2.round(3).to_string())
