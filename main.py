import random
import math
import matplotlib.pyplot as plt
from tqdm import tqdm


class Person:
    def __init__(self, sex):
        self.sex = sex
        self.age = 0
        self.partner = None
        self.children = []
        self.copulated = False

    def fertility(self):
        if self.sex == 'f':
            if self.age < 20:
                return 0.8  # Slightly lower fertility for very young women
            elif 20 <= self.age <= 30:
                return 1.0  # Peak fertility
            elif 31 <= self.age <= 35:
                return 0.8  # Gradual decline begins
            elif 36 <= self.age <= 40:
                return 0.5  # Moderate decline
            elif 41 <= self.age <= 45:
                return 0.2  # Sharp decline
            else:
                return 0.01  # Near menopause, very low fertility
        elif self.sex == 'm':
            if self.age < 20:
                return 0.9  # Slightly lower fertility for very young men
            elif 20 <= self.age <= 35:
                return 1.0  # Peak fertility
            elif 36 <= self.age <= 50:
                return 0.8  # Gradual decline
            elif 51 <= self.age <= 65:
                return 0.3  # Moderate decline
            else:
                return 0.1  # Significant decline with age

    def mortality(self, a=0.005, b=1, c=0.0001, d=0.0001, e=0.077):
        return a * math.exp(- b * self.age) + c + d * math.exp(e * self.age)


def conception_prob(fertility, n_children):
    return min(fertility * 0.25 * 12, 1) / (n_children + 1)


if __name__ == '__main__':
    init_pop_count = 1000
    relationship_prob = 0.1  # per year
    population = []
    for _ in range(init_pop_count // 2):
        population.append(Person('m'))
        population.append(Person('f'))

    init_ages = []
    for p in population:
        age = max(int(random.normalvariate(30, 20)), 0)
        p.age = age
        init_ages.append(age)

    pop_sizes = []
    child_bearing_ages = []
    n_years = 1000
    for _ in tqdm(range(n_years)):
        pop_sizes.append(len(population))
        random.shuffle(population)
        babies = []
        for i in range(len(population) - 1):
            if population[i].age >= 18:
                if not population[i].partner:
                    if 18 <= population[i + 1].age <= population[i].age + 10 and not population[i + 1].partner:
                        if random.random() < relationship_prob and population[i].sex != population[i + 1].sex:
                            population[i].partner = population[i + 1]
                            population[i + 1].partner = population[i]
                else:
                    if not population[i].copulated:
                        population[i].copulated = True
                        population[i].partner.copulated = True
                        if random.random() < conception_prob(
                                population[i].fertility() * population[i].partner.fertility(),
                                len(population[i].children)):
                            if random.random() <= 0.5:
                                baby = Person('m')
                            else:
                                baby = Person('f')
                            child_bearing_ages.append(population[i].age)
                            child_bearing_ages.append(population[i].partner.age)
                            babies.append(baby)
                            population[i].children.append(baby)
                            population[i].partner.children.append(baby)

        population.extend(babies)

        deaths = []
        for p in population:
            if random.random() < p.mortality():
                if p.partner:
                    p.partner.partner = None
                deaths.append(p)
            else:
                p.age += 1
                p.copulated = False

        for p in deaths:
            population.remove(p)

    final_ages = []
    for p in population:
        final_ages.append(p.age)

    plt.figure()
    plt.plot(pop_sizes)
    plt.title('Population')
    plt.xlabel('year')
    plt.ylabel('population')
    plt.show()

    plt.figure()
    plt.hist(child_bearing_ages, bins=20)
    plt.title('Childbearing Age')
    plt.show()

    plt.figure()
    plt.hist(init_ages, bins=20, label='Initial', density=True)
    plt.hist(final_ages, bins=20, alpha=0.5, label='Final', density=True)
    plt.title('Age distribution')
    plt.legend()
    plt.show()
