import random
import matplotlib.pyplot as plt
from tqdm import tqdm


class Person:
    def __init__(self, sex):
        self.sex = sex
        self.lifetime = int(random.normalvariate(80, 5))
        self.age = 0
        self.partner = None
        self.parents = []
        self.siblings = []
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


def conception_prob(fertility, n_children):
    return min(fertility * 0.25 * 12, 1) / (n_children + 1)


if __name__ == '__main__':
    init_pop_count = 1000
    relationship_prob = 0.1  # per year
    population = []
    for _ in range(init_pop_count // 2):
        population.append(Person('m'))
        population.append(Person('f'))

    for p in population:
        p.age = random.randint(0, p.lifetime)

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
            p.age += 1
            p.copulated = False
            if p.age >= p.lifetime:
                if p.partner:
                    p.partner.partner = None
                deaths.append(p)

        for p in deaths:
            population.remove(p)

    plt.figure()
    plt.plot(pop_sizes)
    plt.show()

    plt.figure()
    plt.hist(child_bearing_ages, bins=20)
    plt.show()
