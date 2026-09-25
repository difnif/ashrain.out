# itemfactory/tools/mkseed_h1_geo.py — 고1 공통수학2 도형의 방정식 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h1_geo.py
#     → seeds/h1-2-coord.json      (좌표: 내분점·두 점 사이의 거리·평행/수직 조건·점과 직선 사이의 거리·세 점이 한 직선 위, 5틀)
#     → seeds/h1-2-circle.json     (원: 일반형→중심·반지름·접할 조건·접선의 길이·지름의 양 끝점·원 위의 점에서의 접선, 5틀)
#     → seeds/h1-2-transform.json  (도형의 이동: 원의 평행이동·점의 대칭이동·직선의 대칭이동·평행이동+대칭이동, 4틀)
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402

TRI = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17), (9, 12, 15), (12, 9, 15), (7, 24, 25), (24, 7, 25)]

# ═══════════════════════════════════════════════════════════════════ 1. 좌표
CO = "h1-2-coord"
CO_B = {**HS, "prereq": ["좌표평면", "일차함수의 기울기"], "ops": ["좌표"], "traps": ["내분 비의 순서", "부호"], "tags": ["내분점", "직선의 방정식"]}


def co_t1():
    return T(CO, 1, CO_B, title="선분의 내분점의 좌표",
        skill="AB를 m : n으로 내분하는 점 ((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n)) 공식 쓰기", axis={"두 점": "−6~6", "비": "1 : 2 ~ 3 : 1"}, disc="내분 공식에서 m과 x₂, n과 x₁이 짝임(엇갈림)을 지키는가", diff=2,
        params=[{"name": "x1", "values": {"int": [-5, 5]}}, {"name": "y1", "values": {"int": [-5, 5]}}, {"name": "dx", "values": {"in": NZ(-2, 2)}}, {"name": "dy", "values": {"in": NZ(-2, 2)}}, {"name": "m", "values": {"int": [1, 3]}}, {"name": "n", "values": {"int": [1, 3]}}],
        derive={"mn": "m + n", "px": "x1 + m*dx", "py": "y1 + m*dy", "x2": "x1 + (m + n)*dx", "y2": "y1 + (m + n)*dy", "ans": "x1 + m*dx + y1 + m*dy"},
        constraints=["m != n", "abs(x2) < 10", "abs(y2) < 10", "ans != 0", "ans not in (x1, y1, x2, y2)"], cost=["x1", "y1", "x2", "y2", "m", "n", "px", "py", "ans"], verify=["mn*px == m*x2 + n*x1", "mn*py == m*y2 + n*y1"],
        q="두 점 A({x1}, {y1}), B({x2}, {y2})에 대하여 선분 AB를 {m} : {n}으로 내분하는 점을 P(a, b)라 할 때, a + b의 값을 구하시오.", answer="{ans}",
        sol1="선분 AB를 m : n으로 내분하는 점의 좌표는 ([[frac(m*x2 + n*x1, m + n)]], [[frac(m*y2 + n*y1, m + n)]])이다 — B의 좌표에 m을, A의 좌표에 n을 곱하는 엇갈림에 주의한다. m = {m}, n = {n}을 넣어 계산한다.",
        sol2=[("a = [[frac({m} × {pn(x2)} + {n} × {pn(x1)}, {mn})]] = {px}", "x좌표"), ("b = [[frac({m} × {pn(y2)} + {n} × {pn(y1)}, {mn})]] = {py}", "y좌표"), ("a + b = {ans}", None, ("{ans}", "a + b"))],
        sol3=["P는 A에서 B 쪽으로 전체의 {m}/{mn}만큼 간 점이므로 A와 B 사이에 있고, AP : PB = {m} : {n}이 되는지 좌표의 차로 확인할 수 있다. 따라서 a + b = {ans}이다.", "P({px}, {py})", "a + b = {ans}"],
        model="내분점 P의 좌표는 ([[frac({m} × {pn(x2)} + {n} × {pn(x1)}, {mn})]], [[frac({m} × {pn(y2)} + {n} × {pn(y1)}, {mn})]]) = ({px}, {py})이므로 a + b = {ans}이다.",
        rubric=[("내분점 공식", 3, "P({px}, {py}){eul(py)} 구했다.", "m, n을 바꿔 짝지었으면 인정하지 않는다."), ("합", 2, "a + b = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("m과 x₁, n과 x₂로 짝지음(외분점처럼)", "내분점 공식", "불인정"), ("m + n으로 나누지 않음", "내분점 공식", "불인정"), ("합 계산 실수", "합", "부분")])


def _co2_rows():
    out = {}
    for dx, dy, d in TRI:
        for sx in (1, -1):
            for sy in (1, -1):
                out[f"{dx}_{dy}_{sx}_{sy}"] = {"dx": sx * dx, "dy": sy * dy, "d": d, "adx": dx, "ady": dy}
    return out


CO2_ROWS = _co2_rows()


def co_t2():
    return T(CO, 2, CO_B, title="두 점 사이의 거리",
        skill="AB = √((x₂ − x₁)² + (y₂ − y₁)²)으로 거리 구하기", axis={"좌표의 차": "피타고라스 수 12쌍 × 부호"}, disc="좌표의 차를 제곱해 더하고 제곱근을 취하며, 차의 부호는 제곱에서 사라짐을 아는가", diff=1,
        params=[{"name": "f", "values": {"in": list(CO2_ROWS)}}, {"name": "x1", "values": {"int": [-5, 5]}}, {"name": "y1", "values": {"int": [-5, 5]}}],
        table={"key": "f", "rows": CO2_ROWS},
        derive={"x2": "x1 + dx", "y2": "y1 + dy", "ans": "d", "s2": "adx*adx + ady*ady"},
        constraints=["ans not in (x1, y1, x2, y2)"], cost=["x1", "y1", "x2", "y2", "ans"], verify=["s2 == d*d"],
        q="두 점 A({x1}, {y1}), B({x2}, {y2}) 사이의 거리를 구하시오.", answer="{ans}",
        sol1="두 점 사이의 거리는 x좌표의 차와 y좌표의 차를 두 변으로 하는 직각삼각형의 빗변이다: AB = √((x₂ − x₁)² + (y₂ − y₁)²). 차의 부호는 제곱하면 사라진다.",
        sol2=[("x좌표의 차 {x2} − {pn(x1)} = {dx}, y좌표의 차 {y2} − {pn(y1)} = {dy}", "좌표의 차"), ("AB = [[sqrt(pow({pn(dx)},2) + pow({pn(dy)},2))]] = [[sqrt({s2})]]", "제곱해 더함"), ("= {ans}", None, ("{ans}", "거리"))],
        sol3=["{adx}, {ady}, {d}는 피타고라스 수({adx}² + {ady}² = {d}²)이므로 거리는 {ans}이다.", "{adx}² + {ady}² = {d}²", "AB = {ans}"],
        model="AB = [[sqrt(pow({pn(dx)},2) + pow({pn(dy)},2))]] = [[sqrt({s2})]] = {ans}이다.",
        rubric=[("거리 공식", 3, "√((x₂ − x₁)² + (y₂ − y₁)²)에 대입해 [[sqrt({s2})]]{eul(s2)} 얻었다.", "차의 부호를 제곱 밖으로 두었으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "제곱근 계산 실수면 1점.")],
        pitfalls=[("좌표의 차를 제곱하지 않고 더함", "거리 공식", "불인정"), ("차의 부호를 빼먹어 다른 값을 더함", "거리 공식", "부분"), ("제곱근 계산 실수", "계산", "부분")])


def co_t3():
    return T(CO, 3, CO_B, title="두 직선의 평행·수직 조건 — 상수 a",
        skill="ax + by + c = 0 꼴에서 기울기를 비교(평행: 기울기 같음, 수직: 기울기의 곱 −1)하기", axis={"직선": "계수 ±1~±6", "조건": "평행 / 수직"}, disc="기울기가 같음(평행)과 곱이 −1(수직)을 일반형 계수로 옮겨 세우는가", diff=2,
        params=[{"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "c", "values": {"in": NZ(-6, 6)}}, {"name": "p", "values": {"in": NZ(-6, 6)}}, {"name": "qv", "values": {"in": NZ(-6, 6)}}, {"name": "r", "values": {"in": NZ(-6, 6)}}, {"name": "k", "values": {"in": ["par", "perp"]}}],
        table={"key": "k", "rows": {"par": {"COND": "평행", "LAW": "기울기가 같다: −a/b = −p/q", "w": 1}, "perp": {"COND": "수직", "LAW": "기울기의 곱이 −1: (−a/b)(−p/q) = −1, 즉 ap + bq = 0", "w": 0}}},
        derive={"apar": "b*p/qv", "aperp": "-b*qv/p", "ans": "w*b*p/qv + (1 - w)*(-b*qv/p)", "m2": "-p/qv"},
        constraints=["w == 0 or (b*p) % qv == 0", "w == 1 or (b*qv) % p == 0", "ans != 0", "ans not in (b, c, p, qv, r)", "w == 0 or c*p != r*ans"], cost=["b", "c", "p", "qv", "r", "ans"], verify=["w == 0 or ans*qv == b*p", "w == 1 or ans*p + b*qv == 0"],
        q="두 직선 ax {sgt(b)}y {sgn(c)} = 0, {co(p)}x {sgt(qv)}y {sgn(r)} = 0이 서로 {COND}일 때, 상수 a의 값을 구하시오.", answer="{ans}",
        sol1="직선 ax {sgt(b)}y {sgn(c)} = 0의 기울기는 −a/{b}, 직선 {co(p)}x {sgt(qv)}y {sgn(r)} = 0의 기울기는 {m2}이다. {COND} 조건은 {LAW}. 이를 a에 대해 푼다.",
        sol2=[("기울기: −a/{b}, {m2}", "일반형 → 기울기"), ("{LAW}", "{COND} 조건"), ("a = {ans}", None, ("{ans}", "a"))],
        sol3=["a = {ans}{eul(ans)} 넣으면 첫 직선의 기울기는 {-ans/b}{ika(-ans/b)} 되어 {COND} 조건({LAW})이 성립한다. 따라서 a = {ans}이다.", "기울기 {-ans/b} vs {m2}", "a = {ans}"],
        model="두 직선의 기울기는 −a/{b}, {m2}이고 {COND} 조건은 {LAW}이므로 a = {ans}이다.",
        rubric=[("조건 세우기", 3, "{COND} 조건({LAW})으로 a에 대한 식을 세웠다.", "평행·수직 조건을 바꿨으면 인정하지 않는다."), ("a 구하기", 2, "a = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("수직 조건을 기울기가 같다고 둠", "조건 세우기", "불인정"), ("기울기의 부호(−a/b) 실수", "조건 세우기", "부분"), ("평행 조건에서 x·y 계수를 바꿔 비례식", "조건 세우기", "불인정")])


def co_t4():
    return T(CO, 4, CO_B, title="점과 직선 사이의 거리",
        skill="점 (x₁, y₁)과 직선 ax + by + c = 0 사이의 거리 |ax₁ + by₁ + c|/√(a² + b²) 공식 쓰기", axis={"직선": "3x + 4y + c, 5x + 12y + c, 8x + 15y + c", "점": "−6~6"}, disc="분자에 절댓값, 분모에 √(a² + b²)를 쓰고 c를 빠뜨리지 않는가", diff=2,
        params=[{"name": "f", "values": {"in": ["3-4", "5-12", "8-15", "4-3", "12-5"]}}, {"name": "x0", "values": {"int": [-5, 5]}}, {"name": "y0", "values": {"int": [-5, 5]}}, {"name": "kd", "values": {"int": [1, 6]}}, {"name": "s", "values": {"in": [1, -1]}}],
        table={"key": "f", "rows": {"3-4": {"A": 3, "B": 4, "N": 5}, "5-12": {"A": 5, "B": 12, "N": 13}, "8-15": {"A": 8, "B": 15, "N": 17}, "4-3": {"A": 4, "B": 3, "N": 5}, "12-5": {"A": 12, "B": 5, "N": 13}}},
        derive={"c": "s*kd*N - A*x0 - B*y0", "num": "s*kd*N", "ans": "kd"},
        constraints=["c != 0", "abs(c) < 40", "ans not in (x0, y0, c, A, B)"], cost=["x0", "y0", "c", "num", "ans"], verify=["ans*N == abs(num)", "A*A + B*B == N*N", "num == A*x0 + B*y0 + c"],
        q="점 ({x0}, {y0}){wa(y0)} 직선 {A}x + {B}y {sgn(c)} = 0 사이의 거리를 구하시오.", answer="{ans}",
        sol1="점 (x₁, y₁)과 직선 ax + by + c = 0 사이의 거리는 [[frac(abs(a*x1 + b*y1 + c), sqrt(pow(a,2) + pow(b,2)))]]이다. 분자는 점의 좌표를 직선의 식에 대입한 값의 절댓값, 분모는 √({A}² + {B}²) = {N}이다.",
        sol2=[("분자: |{A} × {pn(x0)} + {B} × {pn(y0)} {sgn(c)}| = |{num}| = {abs(num)}", "대입 후 절댓값"), ("분모: [[sqrt(pow({A},2) + pow({B},2))]] = {N}", "계수의 제곱합의 제곱근"), ("거리 = {abs(num)} ÷ {N} = {ans}", None, ("{ans}", "거리"))],
        sol3=["{A}² + {B}² = {N}²이므로 분모는 정확히 {N}이다. 분자에 절댓값을 붙여 거리가 양수임을 확인한다. 따라서 거리는 {ans}이다.", "|{num}| / {N}", "거리 {ans}"],
        model="거리 = [[frac(abs({A} × {pn(x0)} + {B} × {pn(y0)} {sgn(c)}), sqrt(pow({A},2) + pow({B},2)))]] = [[frac({abs(num)}, {N})]] = {ans}이다.",
        rubric=[("공식 대입", 3, "분자 |{num}|, 분모 {N}{eul(N)} 구했다.", "c를 빠뜨렸거나 절댓값을 빠뜨렸으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("상수항 c를 대입에서 빠뜨림", "공식 대입", "불인정"), ("절댓값 없이 음수 거리", "공식 대입", "부분"), ("분모를 a + b로 둠", "공식 대입", "불인정")])


def co_t5():
    return T(CO, 5, CO_B, title="세 점이 한 직선 위에 있을 조건 — k의 값",
        skill="두 점씩 잡은 기울기가 같다고 놓아 미지수 구하기", axis={"세 점": "−6~6"}, disc="세 점이 한 직선 위 ⇔ AB의 기울기 = AC의 기울기임을 쓰는가", diff=2,
        params=[{"name": "x1", "values": {"int": [-6, 6]}}, {"name": "y1", "values": {"int": [-6, 6]}}, {"name": "d1", "values": {"in": NZ(-4, 4)}}, {"name": "d2", "values": {"in": NZ(-4, 4)}}, {"name": "mn", "values": {"in": NZ(-3, 3)}}, {"name": "md", "values": {"int": [1, 3]}}],
        derive={"x2": "x1 + d1", "y2": "y1 + mn*d1/md", "x3": "x1 + d2", "y3": "y1 + mn*d2/md", "ans": "y1 + mn*d2/md", "slope": "mn/md"},
        constraints=["d1 != d2", "(mn*d1) % md == 0", "(mn*d2) % md == 0", "ans not in (x1, y1, x2, y2, x3)", "ans != 0"], cost=["x1", "y1", "x2", "y2", "x3", "slope", "ans"], verify=["(y2 - y1)*(x3 - x1) == (ans - y1)*(x2 - x1)"],
        q="세 점 A({x1}, {y1}), B({x2}, {y2}), C({x3}, k)가 한 직선 위에 있을 때, k의 값을 구하시오.", answer="{ans}",
        sol1="세 점이 한 직선 위에 있으면 어느 두 점을 잡아도 기울기가 같다. 직선 AB의 기울기는 [[frac({y2} − {pn(y1)}, {x2} − {pn(x1)})]] = {slope}이므로 직선 AC의 기울기 [[frac(k − {pn(y1)}, {x3} − {pn(x1)})]]도 {slope}이어야 한다.",
        sol2=[("AB의 기울기 = [[frac({y2 - y1}, {x2 - x1})]] = {slope}", "두 점의 기울기"), ("AC의 기울기 = [[frac(k − {pn(y1)}, {x3 - x1})]] = {slope}", "기울기 같음"), ("k = {ans}", None, ("{ans}", "k"))],
        sol3=["직선 AB의 방정식 y − {pn(y1)} = {slope}(x − {pn(x1)})에 x = {x3}{eul(x3)} 넣으면 y = {ans}{ika(ans)} 되어 C가 그 직선 위에 있다. 따라서 k = {ans}이다.", "직선 AB에 x = {x3} 대입 → {ans}", "k = {ans}"],
        model="AB의 기울기 {slope}와 AC의 기울기 [[frac(k − {pn(y1)}, {x3 - x1})]]{ika(x3 - x1)} 같아야 하므로 k = {ans}이다.",
        rubric=[("기울기 조건", 3, "AB와 AC의 기울기가 같다는 식을 세웠다.", "기울기의 분모·분자를 바꿨으면 인정하지 않는다."), ("k 구하기", 2, "k = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("기울기의 분자·분모를 바꿈", "기울기 조건", "불인정"), ("좌표의 차 부호 실수", "기울기 조건", "부분"), ("이항 실수", "k 구하기", "부분")])


CO_SEED = SEED(CO, category="함수", title="좌표 — 내분점·두 점 사이의 거리·평행/수직 조건·점과 직선 사이의 거리·세 점이 한 직선 위", unit_id="h1-2", concept_ids=["h1-2-01", "h1-2-02", "h1-2-03"],
               schema_name="좌표평면 위의 점과 직선", note="거리는 피타고라스 수 표(TRI)로 정수 보장. 점·직선 거리는 (3,4,5)·(5,12,13)·(8,15,17) 계수와 분자 나누어떨어짐 제약.",
               templates=[co_t1(), co_t2(), co_t3(), co_t4(), co_t5()])


# ═══════════════════════════════════════════════════════════════════ 2. 원의 방정식
CI = "h1-2-circle"
CI_B = {**HS, "prereq": ["완전제곱식", "점과 직선 사이의 거리"], "ops": ["원의 방정식"], "traps": ["중심 부호", "반지름 제곱"], "tags": ["원의 방정식", "원과 직선"]}


def ci_t1():
    return T(CI, 1, CI_B, title="원의 방정식의 일반형 → 중심과 반지름",
        skill="x² + y² + Ax + By + C = 0을 완전제곱식으로 고쳐 중심과 반지름 읽기", axis={"중심": "−5~5", "반지름": "1~6"}, disc="x, y 각각 (계수의 반)²을 더하고 빼서 (x − a)² + (y − b)² = r² 꼴로 만드는가", diff=2,
        params=[{"name": "p", "values": {"in": NZ(-5, 5)}}, {"name": "qv", "values": {"in": NZ(-5, 5)}}, {"name": "r", "values": {"int": [1, 6]}}, {"name": "k", "values": {"in": ["sum", "r"]}}],
        table={"key": "k", "rows": {"sum": {"ASK": "a + b + r", "w": 1}, "r": {"ASK": "r", "w": 0}}},
        derive={"A": "-2*p", "B": "-2*qv", "C": "p*p + qv*qv - r*r", "ans": "w*(p + qv + r) + (1 - w)*r", "np": "-p", "nq": "-qv", "r2": "r*r"},
        constraints=["C != 0", "ans != 0", "ans not in (A, B, C)"], cost=["p", "qv", "r", "A", "B", "C", "ans"], verify=["A == -2*p", "B == -2*qv", "C == p*p + qv*qv - r2"],
        q="원 x² + y² {sgt(A)}x {sgt(B)}y {sgn(C)} = 0의 중심의 좌표를 (a, b), 반지름의 길이를 r라 할 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="x에 대한 항과 y에 대한 항을 각각 완전제곱식으로 만든다: x² {sgt(A)}x = (x {sgn(np)})² − {p*p}, y² {sgt(B)}y = (y {sgn(nq)})² − {qv*qv}. 정리하면 (x {sgn(np)})² + (y {sgn(nq)})² = {r2}이므로 중심 ({p}, {qv}), 반지름 {r}이다.",
        sol2=[("(x {sgn(np)})² + (y {sgn(nq)})² = {p*p} + {qv*qv} {sgn(-C)} = {r2}", "완전제곱식"), ("중심 ({p}, {qv}), 반지름 [[sqrt({r2})]] = {r}", "표준형 읽기"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["(x {sgn(np)})² + (y {sgn(nq)})² = {r2}{eul(r2)} 전개하면 x² + y² {sgt(A)}x {sgt(B)}y {sgn(C)} = 0으로 원래 식과 같다. 따라서 {ASK} = {ans}이다.", "전개 확인 ✓", "{ASK} = {ans}"],
        model="x² + y² {sgt(A)}x {sgt(B)}y {sgn(C)} = 0을 변형하면 (x {sgn(np)})² + (y {sgn(nq)})² = {r2}이므로 중심은 ({p}, {qv}), 반지름은 {r}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("표준형 변형", 3, "(x {sgn(np)})² + (y {sgn(nq)})² = {r2}{ro(r2)} 고쳤다.", "우변 계산 실수면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "중심의 부호를 반대로 읽었으면 인정하지 않는다.")],
        pitfalls=[("중심을 (A/2, B/2)로 부호 반대", "답", "불인정"), ("반지름을 r²으로 답함", "답", "부분"), ("완전제곱식 만들 때 더한 값을 우변에 반영하지 않음", "표준형 변형", "불인정")])


def ci_t2():
    return T(CI, 2, CI_B, title="원과 직선이 접할 조건 — 상수 k",
        skill="중심과 직선 사이의 거리가 반지름과 같다는 조건 세우기", axis={"원": "중심 ±1~±3, r 1~5", "직선": "3x + 4y + k, 5x + 12y + k, 8x + 15y + k"}, disc="접함 ⇔ (중심과 직선 사이의 거리) = r 임을 쓰고 절댓값을 풀어 양수 k를 고르는가", diff=3,
        params=[{"name": "f", "values": {"in": ["3-4", "5-12", "8-15"]}}, {"name": "p", "values": {"in": NZ(-3, 3)}}, {"name": "qv", "values": {"in": NZ(-3, 3)}}, {"name": "r", "values": {"int": [1, 5]}}],
        table={"key": "f", "rows": {"3-4": {"A": 3, "B": 4, "N": 5}, "5-12": {"A": 5, "B": 12, "N": 13}, "8-15": {"A": 8, "B": 15, "N": 17}}},
        derive={"np": "-p", "nq": "-qv", "r2": "r*r", "S": "A*p + B*qv", "NR": "N*r", "ans": "N*r - A*p - B*qv", "k2": "-N*r - A*p - B*qv"},
        constraints=["abs(S) < NR", "ans not in (r2, A, B, p, qv)"], cost=["p", "qv", "r", "S", "NR", "ans"], verify=["ans == NR - S", "k2 < 0", "ans > 0"],
        q="원 (x {sgn(np)})² + (y {sgn(nq)})² = {r2}{wa(r2)} 직선 {A}x + {B}y + k = 0이 접할 때, 양수 k의 값을 구하시오.", answer="{ans}",
        sol1="원의 중심 ({p}, {qv})와 직선 사이의 거리가 반지름 {r}{wa(r)} 같으면 접한다. 거리 = |{A} × {pn(p)} + {B} × {pn(qv)} + k| / √({A}² + {B}²) = |{S} + k| / {N}이므로 |{S} + k| = {NR}.",
        sol2=[("접함 ⇔ (중심과 직선 사이의 거리) = 반지름", "위치 관계"), ("|{S} + k| / [[sqrt(pow({A},2) + pow({B},2))]] = |{S} + k| / {N} = {r}", "점과 직선 사이의 거리"), ("{S} + k = ±{NR} → k = {ans} 또는 k = {k2}, 양수 k = {ans}", None, ("{ans}", "k"))],
        sol3=["k = {ans}이면 |{S} {sgn(ans)}| / {N} = {NR}/{N} = {r}{ro(r)} 반지름과 같아 접한다. 다른 해 k = {k2}는 음수이므로 조건에 맞지 않는다. 따라서 k = {ans}이다.", "거리 = {NR}/{N} = {r} ✓", "k = {ans}"],
        model="접하려면 중심 ({p}, {qv})와 직선 사이의 거리 |{S} + k|/{N}{ika(N)} 반지름 {r}{wa(r)} 같아야 하므로 {S} + k = ±{NR}, 양수 k = {ans}이다.",
        rubric=[("접할 조건", 3, "|{S} + k|/{N} = {r}{eul(r)} 세웠다.", "판별식 D = 0으로 풀었어도 인정한다."), ("k 구하기", 2, "k = {ans}{eul(ans)} 구했다.", "음수 해를 함께 답했으면 1점.")],
        pitfalls=[("거리 = r²으로 둠", "접할 조건", "불인정"), ("분모를 √(a² + b²) 대신 a + b로 둠", "접할 조건", "불인정"), ("음수 k도 답함", "k 구하기", "부분")])


def _ci3_rows():
    out = {}
    for t, r, d in [(4, 3, 5), (12, 5, 13), (8, 6, 10), (15, 8, 17), (24, 7, 25), (12, 9, 15), (16, 12, 20), (24, 10, 26), (3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17)]:
        for dx, dy in [(a, b) for (a, b, c) in TRI if c == d] if any(c == d for (_, _, c) in TRI) else []:
            for sx in (1, -1):
                out[f"{t}_{r}_{dx}_{dy}_{sx}"] = {"t": t, "r": r, "d": d, "dx": sx * dx, "dy": dy, "d2": d * d, "r2": r * r, "t2": t * t}
    return out


CI3_ROWS = _ci3_rows()


def ci_t3():
    return T(CI, 3, CI_B, title="원 밖의 한 점에서 그은 접선의 길이",
        skill="접선의 길이 = √((중심과 점 사이의 거리)² − r²)로 계산하기", axis={"중심·점 사이 거리": "피타고라스 수", "반지름": "3~12"}, disc="접점에서 접선 ⊥ 반지름이므로 PT² = OP² − r²임을 쓰는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CI3_ROWS)}}, {"name": "p", "values": {"int": [-4, 4]}}, {"name": "qv", "values": {"int": [-4, 4]}}],
        table={"key": "f", "rows": CI3_ROWS},
        derive={"px": "p + dx", "py": "qv + dy", "ans": "t", "np": "-p", "nq": "-qv"},
        constraints=["ans not in (px, py, p, qv, r2)"], cost=["p", "qv", "px", "py", "r", "d", "ans"], verify=["d2 == dx*dx + dy*dy", "t2 + r2 == d2"],
        q="점 P({px}, {py})에서 원 (x {sgn(np)})² + (y {sgn(nq)})² = {r2}에 그은 접선의 접점을 T라 할 때, 선분 PT의 길이를 구하시오.", answer="{ans}",
        sol1="원의 중심 C({p}, {qv}), 반지름 {r}이다. 접점 T에서 반지름 CT와 접선 PT는 수직이므로 직각삼각형 PTC에서 PT² = CP² − CT² = CP² − {r2}. CP = √(({px} − {pn(p)})² + ({py} − {pn(qv)})²) = {d}이다.",
        sol2=[("중심 C({p}, {qv}), r = {r}", "원의 표준형"), ("CP = [[sqrt(pow({pn(dx)},2) + pow({pn(dy)},2))]] = {d}", "두 점 사이의 거리"), ("PT = [[sqrt(pow({d},2) − pow({r},2))]] = [[sqrt({t2})]] = {ans}", None, ("{ans}", "접선의 길이"))],
        sol3=["PT² + CT² = {t2} + {r2} = {d2} = CP²으로 피타고라스 정리를 만족한다. 따라서 PT = {ans}이다.", "{t2} + {r2} = {d2} ✓", "PT = {ans}"],
        model="중심 C({p}, {qv}), 반지름 {r}이고 CP = {d}이므로 PT = [[sqrt(pow({d},2) − pow({r},2))]] = {ans}이다.",
        rubric=[("직각삼각형", 3, "PT² = CP² − r²을 세우고 CP = {d}{eul(d)} 구했다.", "CP를 잘못 구했으면 1점."), ("계산", 2, "PT = {ans}{eul(ans)} 구했다.", "제곱근 계산 실수면 1점.")],
        pitfalls=[("PT = CP − r로 둠", "직각삼각형", "불인정"), ("중심의 부호를 반대로 읽음", "직각삼각형", "부분"), ("제곱근 계산 실수", "계산", "부분")])


def ci_t4():
    return T(CI, 4, CI_B, title="두 점을 지름의 양 끝으로 하는 원의 방정식",
        skill="중심은 두 점의 중점, 반지름은 두 점 사이 거리의 절반임을 써서 일반형의 계수 구하기", axis={"두 점": "−6~6 (좌표 차는 짝수)"}, disc="중점을 중심으로, AB/2를 반지름으로 놓고 전개해 계수를 읽는가", diff=3,
        params=[{"name": "p", "values": {"int": [-5, 5]}}, {"name": "qv", "values": {"int": [-5, 5]}}, {"name": "f", "values": {"in": list(CO2_ROWS)}}],
        table={"key": "f", "rows": CO2_ROWS},
        derive={"x1": "p - dx/2", "y1": "qv - dy/2", "x2": "p + dx/2", "y2": "qv + dy/2", "r": "d/2", "r2": "d*d/4", "A": "-2*p", "B": "-2*qv", "C": "p*p + qv*qv - d*d/4", "ans": "-2*p - 2*qv + p*p + qv*qv - d*d/4", "np": "-p", "nq": "-qv"},
        constraints=["dx % 2 == 0", "dy % 2 == 0", "ans != 0", "ans not in (x1, y1, x2, y2)"], cost=["x1", "y1", "x2", "y2", "p", "qv", "r2", "ans"], verify=["4*r2 == d*d", "ans == A + B + C"],
        q="두 점 A({x1}, {y1}), B({x2}, {y2})를 지름의 양 끝 점으로 하는 원의 방정식이 x² + y² + ax + by + c = 0일 때, 상수 a, b, c에 대하여 a + b + c의 값을 구하시오.", answer="{ans}",
        sol1="지름의 양 끝이 A, B이면 중심은 AB의 중점 ({p}, {qv}), 반지름은 AB의 절반이다. AB = {d}이므로 r = {r}, r² = {r2}. 표준형 (x {sgn(np)})² + (y {sgn(nq)})² = {r2}{eul(r2)} 전개해 계수를 읽는다.",
        sol2=[("중심 = 중점 ({p}, {qv}), AB = {d} → r² = {r2}", "지름 → 중심·반지름"), ("(x {sgn(np)})² + (y {sgn(nq)})² = {r2} → x² + y² {sgt(A)}x {sgt(B)}y {sgn(C)} = 0", "전개"), ("a + b + c = {ans}", None, ("{ans}", "a + b + c"))],
        sol3=["A({x1}, {y1})을 원의 방정식에 넣으면 성립한다(지름의 끝점은 원 위의 점). 따라서 a + b + c = {ans}이다.", "A 대입 → 0 ✓", "a + b + c = {ans}"],
        model="중심은 중점 ({p}, {qv}), 반지름의 제곱은 (AB/2)² = {r2}이므로 원의 방정식은 x² + y² {sgt(A)}x {sgt(B)}y {sgn(C)} = 0이고 a + b + c = {ans}이다.",
        rubric=[("중심·반지름", 3, "중심 ({p}, {qv}), r² = {r2}{eul(r2)} 구했다.", "반지름을 AB로 두었으면 인정하지 않는다."), ("전개·답", 2, "전개해 a + b + c = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("반지름을 AB(지름)로 둠", "중심·반지름", "불인정"), ("중점 계산 실수", "중심·반지름", "부분"), ("전개 실수", "전개·답", "부분")])


def ci_t5():
    return T(CI, 5, CI_B, title="원 위의 점에서의 접선의 방정식 — 절편",
        skill="원 x² + y² = r² 위의 점 (x₁, y₁)에서의 접선 x₁x + y₁y = r²을 쓰기", axis={"접점": "피타고라스 수 (3,4,5)·(6,8,10)·(5,12,13)"}, disc="접선의 방정식 x₁x + y₁y = r²을 쓰고 절편을 바르게 읽는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CO2_ROWS)}}, {"name": "k", "values": {"in": ["x", "y"]}}],
        table=[{"key": "f", "rows": CO2_ROWS}, {"key": "k", "rows": {"x": {"ASK": "x절편", "SET": "y = 0", "VAR": "x", "w": 1}, "y": {"ASK": "y절편", "SET": "x = 0", "VAR": "y", "w": 0}}}],
        derive={"x1": "dx", "y1": "dy", "r2": "d*d", "den": "w*dx + (1 - w)*dy", "ans": "(d*d)/(w*dx + (1 - w)*dy)"},
        constraints=["ans not in (x1, y1, r2)"], cost=["x1", "y1", "r2", "ans"], verify=["x1*x1 + y1*y1 == r2", "ans*den == r2"],
        q="원 x² + y² = {r2} 위의 점 ({x1}, {y1})에서의 접선의 {ASK}을 구하시오.", answer="{ans}",
        sol1="원 x² + y² = r² 위의 점 (x₁, y₁)에서의 접선의 방정식은 x₁x + y₁y = r²이다. 따라서 접선은 {co(x1)}x {sgt(y1)}y = {r2}이고, x절편은 y = 0, y절편은 x = 0을 넣어 구한다.",
        sol2=[("접선: {co(x1)}x {sgt(y1)}y = {r2}", "x₁x + y₁y = r²"), ("{SET}을 넣으면 {VAR} × {pn(den)} = {r2}", "절편"), ("{ASK} = {r2} ÷ {pn(den)} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["접점 ({x1}, {y1})을 접선에 넣으면 {pn(x1)}² + {pn(y1)}² = {r2}{ro(r2)} 성립하고, 접선은 반지름(기울기 {y1}/{x1})에 수직이다. 따라서 {ASK} = {ans}이다.", "접점 대입 ✓", "{ASK} = {ans}"],
        model="접선의 방정식은 {co(x1)}x {sgt(y1)}y = {r2}이므로 {SET}을 넣어 {ASK}은 {ans}이다.",
        rubric=[("접선의 방정식", 3, "{co(x1)}x {sgt(y1)}y = {r2}{eul(r2)} 세웠다.", "우변을 r로 두었으면 1점."), ("절편", 2, "{ASK} {ans}{eul(ans)} 구했다.", "x·y절편을 바꿨으면 인정하지 않는다.")],
        pitfalls=[("우변을 r로 둠", "접선의 방정식", "부분"), ("접점을 지나는 반지름의 방정식을 씀", "접선의 방정식", "불인정"), ("x·y절편 혼동", "절편", "불인정")])


CI_SEED = SEED(CI, category="함수", title="원의 방정식 — 일반형→중심·반지름·접할 조건·접선의 길이·지름의 양 끝·원 위의 점에서의 접선", unit_id="h1-2", concept_ids=["h1-2-04", "h1-2-05"],
               schema_name="원의 방정식과 원과 직선의 위치 관계", note="중심·반지름을 파라미터로 잡고 일반형 계수를 파생. 접선의 길이·지름은 피타고라스 수 표.",
               templates=[ci_t1(), ci_t2(), ci_t3(), ci_t4(), ci_t5()])


# ═══════════════════════════════════════════════════════════════════ 3. 도형의 이동
TR = "h1-2-transform"
TR_B = {**HS, "prereq": ["원의 방정식", "직선의 방정식"], "ops": ["도형의 이동"], "traps": ["이동 방향 부호", "대칭의 종류"], "tags": ["평행이동", "대칭이동"]}


def _sq(v, c):
    """원의 방정식 문면 — 중심 좌표 c 에 대한 (v − c)², c = 0 이면 v² ('(x + 0)²' 을 쓰지 않는다)."""
    return f"{v}²" if c == 0 else f"({v} {'−' if c > 0 else '+'} {abs(c)})²"


def tr_t1():
    return T(TR, 1, TR_B, title="원의 평행이동 — 옮긴 원의 방정식의 상수항",
        skill="x 대신 x − m, y 대신 y − n을 넣어 옮긴 도형의 식을 만들고 전개하기", axis={"중심": "−4~4", "이동": "±1~±5"}, disc="x축 방향 m만큼의 이동이 x → x − m임을 알고 중심이 (p + m, q + n)이 됨을 쓰는가", diff=2,
        table=[{"key": "p", "rows": {str(v): {"XL": _sq("x", v)} for v in range(-4, 5)}}, {"key": "qv", "rows": {str(v): {"YL": _sq("y", v)} for v in range(-4, 5)}}],
        params=[{"name": "p", "values": {"int": [-4, 4]}}, {"name": "qv", "values": {"int": [-4, 4]}}, {"name": "r", "values": {"int": [1, 5]}}, {"name": "m", "values": {"in": NZ(-5, 5)}}, {"name": "n", "values": {"in": NZ(-5, 5)}}],
        derive={"np": "-p", "nq": "-qv", "r2": "r*r", "p2": "p + m", "q2": "qv + n", "np2": "-(p + m)", "nq2": "-(qv + n)", "A": "-2*(p + m)", "B": "-2*(qv + n)", "ans": "(p + m)**2 + (qv + n)**2 - r*r"},
        constraints=["ans != 0", "ans not in (p, qv, r2, m, n)", "p2 != 0", "q2 != 0"], cost=["p", "qv", "r", "m", "n", "p2", "q2", "ans"], verify=["ans == p2*p2 + q2*q2 - r2"],
        q="원 {XL} + {YL} = {r2}{eul(r2)} x축의 방향으로 {m}만큼, y축의 방향으로 {n}만큼 평행이동한 원의 방정식이 x² + y² + ax + by + c = 0일 때, 상수 c의 값을 구하시오.", answer="{ans}",
        sol1="도형을 x축의 방향으로 {m}만큼, y축의 방향으로 {n}만큼 평행이동하면 식의 x 대신 x {sgn(-m)}, y 대신 y {sgn(-n)}{eul(n)} 넣는다. 원의 중심 ({p}, {qv}){eun(qv)} ({p2}, {q2}){ro(q2)} 옮겨지고 반지름은 그대로 {r}이다. (x {sgn(np2)})² + (y {sgn(nq2)})² = {r2}{eul(r2)} 전개해 상수항을 읽는다.",
        sol2=[("중심 ({p}, {qv}) → ({p2}, {q2}), 반지름 {r} 그대로", "평행이동"), ("(x {sgn(np2)})² + (y {sgn(nq2)})² = {r2}", "옮긴 원"), ("전개: x² + y² {sgt(A)}x {sgt(B)}y {sgn(ans)} = 0 → c = {ans}", None, ("{ans}", "c"))],
        sol3=["상수항 c = (중심의 x좌표)² + (중심의 y좌표)² − (반지름)² = {pn(p2)}² + {pn(q2)}² − {r2} = {ans}이다. 따라서 c = {ans}이다.", "c = {pn(p2)}² + {pn(q2)}² − {r2}", "c = {ans}"],
        model="평행이동한 원은 (x {sgn(np2)})² + (y {sgn(nq2)})² = {r2}이고 전개하면 x² + y² {sgt(A)}x {sgt(B)}y {sgn(ans)} = 0이므로 c = {ans}이다.",
        rubric=[("평행이동", 3, "옮긴 원 (x {sgn(np2)})² + (y {sgn(nq2)})² = {r2}{eul(r2)} 세웠다.", "이동 방향 부호가 반대면 인정하지 않는다."), ("전개·c", 2, "c = {ans}{eul(ans)} 구했다.", "전개 실수면 1점.")],
        pitfalls=[("x 대신 x {sgn(m)}, y 대신 y {sgn(n)}{eul(n)} 넣음(방향 반대)", "평행이동", "불인정"), ("반지름도 바뀐다고 생각함", "평행이동", "부분"), ("전개 실수", "전개·c", "부분")])


SYM_ROWS = {
    "x": {"SYM": "x축", "RULE": "(a, b) → (a, −b)", "wx": 1, "wy": -1, "sw": 0},
    "y": {"SYM": "y축", "RULE": "(a, b) → (−a, b)", "wx": -1, "wy": 1, "sw": 0},
    "o": {"SYM": "원점", "RULE": "(a, b) → (−a, −b)", "wx": -1, "wy": -1, "sw": 0},
    "yx": {"SYM": "직선 y = x", "RULE": "(a, b) → (b, a)", "wx": 1, "wy": 1, "sw": 1},
}


def tr_t2():
    return T(TR, 2, TR_B, title="점의 대칭이동 — x축·y축·원점·직선 y = x",
        skill="대칭의 종류에 따라 좌표의 부호를 바꾸거나 x, y를 서로 바꾸기", axis={"점": "±1~±7", "대칭": "4가지"}, disc="x축 대칭은 y의 부호, y축 대칭은 x의 부호, 원점은 둘 다, y = x는 자리 바꿈임을 구별하는가", diff=1,
        params=[{"name": "a", "values": {"in": NZ(-7, 7)}}, {"name": "b", "values": {"in": NZ(-7, 7)}}, {"name": "k", "values": {"in": list(SYM_ROWS)}}],
        table={"key": "k", "rows": SYM_ROWS},
        derive={"x2": "(1 - sw)*wx*a + sw*b", "y2": "(1 - sw)*wy*b + sw*a", "ans": "(1 - sw)*(wx*a + wy*b) + sw*(a + b) + 0*((1 - sw)*wx*a + sw*b)"},
        constraints=["a != b", "a != -b", "ans != 0", "ans not in (a, b)"], cost=["a", "b", "x2", "y2", "ans"], verify=["ans == x2 + y2"],
        q="점 ({a}, {b}){eul(b)} {SYM}에 대하여 대칭이동한 점의 좌표를 (p, q)라 할 때, p − q의 값을 구하시오.", answer="{ans2}",
        sol1="{SYM}에 대한 대칭이동: {RULE}. 따라서 점 ({a}, {b})는 ({x2}, {y2})로 옮겨진다.",
        sol2=[("{SYM} 대칭: {RULE}", "대칭의 규칙"), ("({a}, {b}) → ({x2}, {y2})", "적용"), ("p − q = {x2} − {pn(y2)} = {ans2}", None, ("{ans2}", "p − q"))],
        sol3=["대칭이동한 점과 원래 점을 이은 선분의 중점이 대칭축(또는 원점) 위에 있는지 확인하면 {SYM} 대칭이 맞다. 따라서 p − q = {ans2}이다.", "중점이 {SYM} 위 ✓", "p − q = {ans2}"],
        model="{SYM}에 대하여 대칭이동하면 ({a}, {b}) → ({x2}, {y2})이므로 p − q = {ans2}이다.",
        rubric=[("대칭 규칙", 3, "{RULE}{eul(RULE)} 적용해 ({x2}, {y2}){eul(y2)} 구했다.", "다른 대칭의 규칙을 썼으면 인정하지 않는다."), ("계산", 2, "p − q = {ans2}{eul(ans2)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("x축 대칭에서 x의 부호를 바꿈", "대칭 규칙", "불인정"), ("y = x 대칭에서 부호까지 바꿈", "대칭 규칙", "불인정"), ("p − q 부호 실수", "계산", "부분")])


def tr_t2_final():
    t = tr_t2()
    t["derive"]["ans2"] = "(1 - sw)*(wx*a - wy*b) + sw*(b - a)"
    t["derive"]["ans"] = "(1 - sw)*(wx*a - wy*b) + sw*(b - a)"
    t["verify"] = ["ans2 == x2 - y2"]
    t["constraints"] = ["a != b", "a != -b", "ans2 != 0", "ans2 not in (a, b)"]
    t["cost_values"] = ["a", "b", "x2", "y2", "ans2"]
    t["answer_var"] = "ans2"
    return t


def tr_t3():
    return T(TR, 3, TR_B, title="직선의 대칭이동 — 대칭이동한 직선 y = ax + b의 a + b",
        skill="x축(y → −y)·y축(x → −x)·원점(둘 다)·직선 y = x(x ↔ y) 대칭으로 식을 바꾸고 y에 대해 정리하기", axis={"직선": "y = mx + n", "대칭": "x축 / y축 / 원점 / y = x"}, disc="대칭의 종류에 맞게 식의 x, y를 바꾼 뒤 y에 대해 정리해 기울기와 y절편을 읽는가", diff=2,
        params=[{"name": "m", "values": {"in": NZ(-5, 5)}}, {"name": "n", "values": {"in": NZ(-7, 7)}}, {"name": "k", "values": {"in": ["x", "y", "o", "yx"]}}],
        table={"key": "k", "rows": {"x": {"SYM": "x축", "RULE": "y 대신 −y", "wa": -1, "wb": -1, "sw": 0}, "y": {"SYM": "y축", "RULE": "x 대신 −x", "wa": -1, "wb": 1, "sw": 0},
                                    "o": {"SYM": "원점", "RULE": "x 대신 −x, y 대신 −y", "wa": 1, "wb": -1, "sw": 0}, "yx": {"SYM": "직선 y = x", "RULE": "x와 y를 서로 바꿈", "wa": 1, "wb": 1, "sw": 1}}},
        derive={"a2": "(1 - sw)*wa*m + sw/m", "b2": "(1 - sw)*wb*n - sw*n/m", "ans": "(1 - sw)*(wa*m + wb*n) + sw*(1 - n)/m", "nm": "-m", "nn": "-n"},
        constraints=["m*m != 1", "ans != 0", "ans not in (m, n)"], cost=["m", "n", "a2", "b2", "ans"], verify=["ans == a2 + b2", "sw == 1 or a2 == wa*m", "sw == 0 or a2*m == 1"],
        q="직선 y = {co(m)}x {sgn(n)}{eul(n)} {SYM}에 대하여 대칭이동한 직선의 방정식이 y = ax + b일 때, 상수 a, b에 대하여 a + b의 값을 구하시오.", answer="{ans}",
        sol1="{SYM}에 대한 대칭이동은 식에서 {RULE}으로 바꾸는 것이다. 바뀐 식을 y에 대해 정리하면 기울기 a와 y절편 b를 읽을 수 있다.",
        sol2=[("{RULE}: 대칭이동한 직선의 식을 만든다", "{SYM} 대칭"), ("y에 대해 정리: y = {co(a2)}x {sgn(b2)}", "a = {a2}, b = {b2}"), ("a + b = {ans}", None, ("{ans}", "a + b"))],
        sol3=["원래 직선 위의 점 (0, {n})을 {SYM}에 대하여 대칭이동한 점이 y = {co(a2)}x {sgn(b2)} 위에 있는지 대입해 확인할 수 있다. 따라서 a + b = {ans}이다.", "y = {co(a2)}x {sgn(b2)}", "a + b = {ans}"],
        model="{SYM}에 대하여 대칭이동하면 {RULE}이므로 대칭이동한 직선은 y = {co(a2)}x {sgn(b2)}이고 a + b = {ans}이다.",
        rubric=[("대칭이동한 식", 3, "{RULE}으로 바꿔 정리한 식이 y = {co(a2)}x {sgn(b2)}이다.", "다른 대칭의 규칙을 썼으면 인정하지 않는다."), ("합", 2, "a + b = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("x축 대칭에서 x의 부호를 바꿈", "대칭이동한 식", "불인정"), ("y = x 대칭 후 y에 대해 정리하지 않고 계수를 읽음", "대칭이동한 식", "부분"), ("부호 실수", "합", "부분")])


def tr_t4():
    return T(TR, 4, TR_B, title="평행이동과 대칭이동의 합성 — 옮긴 원의 중심",
        skill="원의 중심을 차례로 옮겨(평행이동 → 대칭이동) 최종 중심의 좌표 구하기", axis={"중심": "−5~5", "이동": "±1~±5", "대칭": "x축 / y축 / y = x"}, disc="이동의 순서를 지키고 각 단계의 규칙을 바르게 적용하는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-5, 5)}}, {"name": "qv", "values": {"in": NZ(-5, 5)}}, {"name": "m", "values": {"in": NZ(-5, 5)}}, {"name": "n", "values": {"in": NZ(-5, 5)}}, {"name": "k", "values": {"in": ["x", "y", "yx"]}}],
        table={"key": "k", "rows": {"x": {"SYM": "x축", "RULE": "(a, b) → (a, −b)", "wx": 1, "wy": -1, "sw": 0}, "y": {"SYM": "y축", "RULE": "(a, b) → (−a, b)", "wx": -1, "wy": 1, "sw": 0}, "yx": {"SYM": "직선 y = x", "RULE": "(a, b) → (b, a)", "wx": 1, "wy": 1, "sw": 1}}},
        derive={"np": "-p", "nq": "-qv", "p1": "p + m", "q1": "qv + n", "x2": "(1 - sw)*wx*(p + m) + sw*(qv + n)", "y2": "(1 - sw)*wy*(qv + n) + sw*(p + m)", "ans": "(1 - sw)*(wx*(p + m) + wy*(qv + n)) + sw*(p + m + qv + n)"},
        constraints=["p1 != 0", "q1 != 0", "p1 != q1", "ans != 0", "ans not in (p, qv, m, n)"], cost=["p", "qv", "m", "n", "p1", "q1", "x2", "y2", "ans"], verify=["ans == x2 + y2"],
        q="원 (x {sgn(np)})² + (y {sgn(nq)})² = 4를 x축의 방향으로 {m}만큼, y축의 방향으로 {n}만큼 평행이동한 후 {SYM}에 대하여 대칭이동한 원의 중심의 좌표를 (a, b)라 할 때, a + b의 값을 구하시오.", answer="{ans}",
        sol1="원의 이동은 중심의 이동으로 추적하면 된다(반지름은 변하지 않는다). 중심 ({p}, {qv})를 평행이동하면 ({p1}, {q1}), 이어서 {SYM} 대칭({RULE})하면 ({x2}, {y2})이다.",
        sol2=[("평행이동: ({p}, {qv}) → ({p1}, {q1})", "x + {m}, y + {n}"), ("{SYM} 대칭: ({p1}, {q1}) → ({x2}, {y2})", "{RULE}"), ("a + b = {ans}", None, ("{ans}", "a + b"))],
        sol3=["순서를 바꿔(대칭 후 평행이동) 계산하면 일반적으로 다른 점이 나오므로 문제의 순서대로 옮겨야 한다. 따라서 a + b = {ans}이다.", "순서: 평행이동 → 대칭", "a + b = {ans}"],
        model="중심 ({p}, {qv})를 평행이동하면 ({p1}, {q1}), {SYM}에 대하여 대칭이동하면 ({x2}, {y2})이므로 a + b = {ans}이다.",
        rubric=[("두 이동", 3, "({p1}, {q1}) → ({x2}, {y2}){ro(y2)} 차례로 옮겼다.", "한 단계만 맞으면 1점."), ("합", 2, "a + b = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("이동 순서를 바꿈", "두 이동", "불인정"), ("평행이동 방향 부호 반대", "두 이동", "부분"), ("대칭 규칙 혼동", "두 이동", "부분")])


TR_SEED = SEED(TR, category="함수", title="도형의 이동 — 원의 평행이동·점의 대칭이동·직선의 대칭이동·평행이동과 대칭이동의 합성", unit_id="h1-2", concept_ids=["h1-2-06", "h1-2-07"],
               schema_name="평행이동과 대칭이동", note="대칭 규칙은 행 표의 가중치(wx, wy, sw)로 좌표를 파생.",
               templates=[tr_t1(), tr_t2_final(), tr_t3(), tr_t4()])


if __name__ == "__main__":
    run(CO_SEED, CI_SEED, TR_SEED)
