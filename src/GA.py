import numpy as np
import src.problem.SCH  as SCH
import src.problem.ZDT1 as ZDT1
import src.problem.ZDT2 as ZDT2
import src.problem.ZDT4 as ZDT4

'''
遗传算法部分
'''
c_rate = 1
m_rate = 0.3
test_fun = ZDT1

idv = -1


def cross(p1, p2):
    # p1 tp p2
    if np.random.rand() < c_rate:
        p2 = idv.reset_one(p2)
        r1 = 0.5 + 0.5 * np.random.rand()
        r2 = 1 - r1
        x2 = r2 * p1.X + r1 * p2.X
        p2.X = x2
        p2.F_value = test_fun.Func(p2.X)
    return p2


def mutate(p):
    # 对p节点变异
    gen_len = len(p.X)
    if np.random.rand() < m_rate:
        p = idv.reset_one(p)
        # 变异5%的基因对
        for l in range(int(gen_len * 0.05)):
            j = np.random.randint(0, gen_len, size=1)[0]
            d = np.random.randint(0, gen_len, size=1)[0]
            p.X[j], p.X[d] = p.X[d], p.X[j]
            p.F_value = test_fun.Func(p.X)
    return p


def select(P):
    # 洗牌产生新P
    i = 0
    while i < len(P) - 1:
        p = P[i]
        p_next = P[i + 1]
        # p dominate p_next
        if p.p_rank < p_next.p_rank or (p.p_rank == p_next.p_rank and p.dp > p_next.dp):
            P[i + 1] = cross(p, p_next)
        elif p.p_rank > p_next.p_rank or (p.p_rank == p_next.p_rank and p.dp < p_next.dp):
            P[i] = cross(p_next, p)
        i += 2
    return P


def next_P(P):
    n_P = []
    p_size = len(P)
    for p in P:
        p = idv.reset_one(p)
        cp = idv.creat_one()
        cp.X = p.X
        cp.F_value = p.F_value
        n_P.append(cp)
    # 产生下一代
    for i in range(p_size):
        j = np.random.randint(0, p_size, size=1)[0]
        n_P[j] = cross(n_P[i], n_P[j])
        n_P[j] = mutate(n_P[i])
        select(n_P)
    return n_P
