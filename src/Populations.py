from src.Individual import *
from src.GA import *


class Population:
    pop_size = 100

    idv = Individual()

    def __init__(self):
        pass

    def creat_pop(self):
        P = []
        for i in range(self.pop_size):
            P.append(self.idv.creat_one())
        return P

    def next_Pop(self, Pop):
        n_P = []
        idv = self.idv
        P = Pop
        p_size = len(P)
        for p in P:
            p = idv.reset_one(p)
            cp = idv.creat_one()
            cp.X[:] = p.X[:]
            cp.F_value[:] = p.F_value[:]
            n_P.append(cp)
        # 产生下一代
        for i in range(p_size):
            j = np.random.randint(0, p_size, size=1)[0]
            n_P[j] = cross(n_P[i], n_P[j])
            n_P[j] = mutate(n_P[j])
            select(n_P)
        return n_P
