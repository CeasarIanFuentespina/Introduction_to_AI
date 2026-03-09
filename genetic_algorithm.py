
"""
Genetic Algorithm (GA)
=====================
The Genetic Algorithm is an evolutionary computation technique that 
mimics natural selection to solve optimization problems.
"""

import random
import json
from typing import List, Tuple


def fitness_function(individual: List[int], target_sum: int) -> float:
    """Calculate fitness based on how close the sum is to target."""
    current_sum = sum(individual)
    return abs(target_sum - current_sum)


def create_individual(gene_count: int, gene_range: Tuple[int, int]) -> List[int]:
    """Create a random individual."""
    return [random.randint(gene_range[0], gene_range[1]) for _ in range(gene_count)]


def selection(population: List[Tuple[List[int], float]], num_parents: int) -> List[List[int]]:
    """Select the best individuals for reproduction (tournament selection)."""
    selected = []
    for _ in range(num_parents):
        tournament = random.sample(population, min(3, len(population)))
        winner = min(tournament, key=lambda x: x[1])
        selected.append(winner[0])
    return selected


def crossover(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
    """Perform single-point crossover between two parents."""
    if len(parent1) < 2:
        return parent1, parent2
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(individual: List[int], mutation_rate: float, gene_range: Tuple[int, int]) -> List[int]:
    """Apply mutation to an individual."""
    mutated = individual[:]
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = random.randint(gene_range[0], gene_range[1])
    return mutated


def genetic_algorithm(target_sum: int, gene_count: int, gene_range: Tuple[int, int],
                     population_size: int = 100, generations: int = 50,
                     mutation_rate: float = 0.1) -> Tuple[List[int], int]:
    """
    Run the genetic algorithm to find numbers that sum to target.
    """
    population = [(create_individual(gene_count, gene_range), float('inf')) 
                   for _ in range(population_size)]
    
    for generation in range(generations):
        population = [(ind, fitness_function(ind, target_sum)) for ind, _ in population]
        population.sort(key=lambda x: x[1])
        
        if population[0][1] == 0:
            return population[0][0], generation
        
        parents = selection(population, population_size // 2)
        
        new_population = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = crossover(parents[i], parents[i + 1])
            child1 = mutate(child1, mutation_rate, gene_range)
            child2 = mutate(child2, mutation_rate, gene_range)
            new_population.append((child1, float('inf')))
            new_population.append((child2, float('inf')))
        
        population = new_population[:population_size - 2]
        population.append(population[0])
        population.append(population[1] if len(population) > 1 else population[0])
    
    population.sort(key=lambda x: x[1])
    return population[0][0], generations


# ==================== EXAMPLE 1: Find Numbers that Sum to Target ====================
print("=" * 60)
print("EXAMPLE 1: Sum Target Problem")
print("=" * 60)

random.seed(42)
target1 = 100
gene_count1 = 5
gene_range1 = (1, 30)

print(f"\nTarget Sum: {target1}")
print(f"Number of Genes: {gene_count1}")
print(f"Gene Range: {gene_range1}")

result1, gen1 = genetic_algorithm(target1, gene_count1, gene_range1)
sum_result1 = sum(result1)

print(f"\nSolution Found at Generation: {gen1}")
print(f"Individual: {result1}")
print(f"Sum: {sum_result1}")
print(f"Fitness: {abs(target1 - sum_result1)}")


# ==================== EXAMPLE 2: Knapsack Problem ====================
print("\n" + "=" * 60)
print("EXAMPLE 2: Knapsack Problem (Genetic Algorithm)")
print("=" * 60)

items = [
    (2, 10), (3, 5), (5, 15), (7, 7), (1, 6),
    (4, 18), (6, 3), (8, 25), (2, 12), (5, 8)
]
max_weight = 15
population_size = 50
generations = 30

print(f"\nItems (weight, value): {items}")
print(f"Max Weight Capacity: {max_weight}")
print(f"Population Size: {population_size}")
print(f"Generations: {generations}")


def knapsack_fitness(individual: List[int]) -> float:
    total_weight = 0
    total_value = 0
    for i, gene in enumerate(individual):
        if gene == 1:
            total_weight += items[i][0]
            total_value += items[i][1]
    
    if total_weight > max_weight:
        return -total_value
    return total_value


def create_knapsack_individual() -> List[int]:
    return [random.randint(0, 1) for _ in range(len(items))]


def knapsack_ga(population_size: int, generations: int) -> Tuple[List[int], int]:
    population = [(create_knapsack_individual(), knapsack_fitness(create_knapsack_individual())) 
                  for _ in range(population_size)]
    
    best_solution = []
    best_value = 0
    
    for generation in range(generations):
        population = [(ind, knapsack_fitness(ind)) for ind, _ in population]
        population.sort(key=lambda x: x[1], reverse=True)
        
        if population[0][1] > best_value:
            best_value = population[0][1]
            best_solution = population[0][0]
        
        parents = selection(population, population_size // 2)
        
        new_population = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = crossover(parents[i], parents[i + 1])
            child1 = mutate(child1, 0.05, (0, 1))
            child2 = mutate(child2, 0.05, (0, 1))
            new_population.append((child1, float('-inf')))
            new_population.append((child2, float('-inf')))
        
        population = new_population[:population_size - 2]
        population.append((best_solution, float('-inf')))
        if len(population) > 1:
            population.append(population[0])
    
    return best_solution, best_value


result2, value2 = knapsack_ga(population_size, generations)

selected_items = [items[i] for i in range(len(result2)) if result2[i] == 1]
total_weight = sum(item[0] for item in selected_items)

print(f"\nBest Solution Found:")
print(f"Selected Items (binary): {result2}")
print(f"Items Selected: {selected_items}")
print(f"Total Weight: {total_weight}")
print(f"Total Value: {value2}")


# ==================== OUTPUT TO JSON ====================
output = {
    "algorithm": "Genetic Algorithm (GA)",
    "examples": [
        {
            "example": 1,
            "description": "Sum Target Problem",
            "target_sum": target1,
            "gene_count": gene_count1,
            "gene_range": gene_range1,
            "result": result1,
            "sum": sum(result1),
            "generation_found": gen1
        },
        {
            "example": 2,
            "description": "Knapsack Problem",
            "items": items,
            "max_weight": max_weight,
            "selected_items": selected_items,
            "total_weight": total_weight,
            "total_value": value2
        }
    ]
}

with open('genetic_algorithm_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n" + "=" * 60)
print("Results saved to genetic_algorithm_results.json")
print("=" * 60)

