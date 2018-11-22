import numpy as np


class GeneticAlgorithm():
    Pop_Size = 0
    Cross_Rate = 0.00
    MUTATION_Rate = 0.00
    Generation_Num = 0

    fitness = []  # 记录种群适应度
    best_child = []
    pop = []  # 记录种群适应度
    max_fitness = 0  # 记录种群最大适应度
    var_fitness = 0  # 记录种群方差
    avg_fitness = 0  # 记录种群平均值

    def __init__(self, valuable_num, X_Bound, pop_size, cross_rate, mutation_rate, generation_num, below):
        self.var_num = valuable_num
        self.X_Bound = X_Bound
        self.Pop_Size = pop_size
        self.Cross_Rate = cross_rate
        self.MUTATION_Rate = mutation_rate
        self.Generation_Num = generation_num
        self.below = below

    def create_init_pop(self, bound, row, cloum):
        cld_x = bound[0] + (bound[1] - bound[0]) * np.random.rand(row, cloum)
        return cld_x

    def Func(self, X):
        return X
    

    def get_fitness(self, pop):
        Z = self.Func(pop)
        fitness = np.max(Z) + 1 - Z
        return fitness

    def sl_pop_by_roulette(self, pop):
        probility = self.fitness / self.fitness.sum()
        idx = np.random.choice(np.arange(self.Pop_Size), size=self.Pop_Size, replace=True, p=probility)
        return pop[:, idx]

    def sl_pop_by_proportion(self, pop):
        probility = self.fitness / self.fitness.sum()
        parg = np.argsort(probility)  # 从小到大的概率索引
        devide = int(self.Pop_Size * 0.3)
        max_fitness_index = parg[-1]
        below_id = parg[:devide]
        max = pop[:, max_fitness_index][:, np.newaxis]
        pop[:, below_id] = max
        return pop

    def mutate(self, pop, m_bound):
        if np.random.rand() < self.MUTATION_Rate:
            for i in range(int(self.var_num * 0.1)):
                j = np.random.randint(0, self.var_num, size=1)[0]
                d = np.random.randint(0, self.var_num, size=1)[0]
                pop[j] = pop[d]

    def crossover_pop(self, pop1, pop2, m_bound):
        if np.random.rand() < self.Cross_Rate:
            p1_f = self.Func(pop1)
            p2_f = self.Func(pop2)
            r1 = 0.5 + 0.5 * np.random.rand()
            if p1_f > p2_f:
                r1 = 1 - r1
            r2 = 1 - r1
            x1 = r1 * pop1 + r2 * pop2
            x2 = r2 * pop1 + r1 * pop2
            x1[x1 > m_bound[1]] = m_bound[1]
            x1[x1 < m_bound[0]] = m_bound[0]
            x2[x2 > m_bound[1]] = m_bound[1]
            x2[x2 < m_bound[0]] = m_bound[0]
            if np.random.rand() < self.Cross_Rate:
                x1_f = self.Func(x1)
                x2_f = self.Func(x2)
                if x1_f < p1_f:
                    pop1[:] = x1[:]
                if x2_f < p2_f:
                    pop2[:] = x2[:]
            else:
                pop1[:] = x1[:]
                pop2[:] = x2[:]
        return pop1, pop2

    def EO(self, pop, rd_bound, step=0.5):
        worstfitness = self.Func(pop)
        m = pop.shape[0]
        for i in range(m):
            tempworst = np.copy(pop)
            tempworst[i] = tempworst[i] + np.random.normal(0, step, 1)
            tempworst[tempworst > rd_bound[1]] = rd_bound[1]
            tempworst[tempworst < rd_bound[0]] = rd_bound[0]
            f = self.Func(tempworst)
            if f < worstfitness:
                worstfitness = f
                pop[:] = tempworst
        return pop
