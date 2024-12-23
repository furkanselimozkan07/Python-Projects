import random
import os

class Item:
    def __init__(self, weight, profit):
        self.weight = weight
        self.profit = profit
        self.unit_price = profit / weight if weight != 0 else 0

    def __repr__(self):
        return f"Item(weight={self.weight}, profit={self.profit}, unit_price={self.unit_price:.2f})"

class Knapsack:
    def __init__(self, capacity):
        self.capacity = capacity

    def random_solution(self, items):
        if not items:
            return 0  # Return zero profit if there are no items

        remaining_capacity = self.capacity
        total_profit = 0

        while remaining_capacity > 0 and items:
            item = random.choice(items)
            if item.weight <= remaining_capacity:
                total_profit += item.profit
                remaining_capacity -= item.weight

        return total_profit

    def greedy_solution(self, items):
        if not items:
            return 0  # Return zero profit if there are no items

        sorted_items = sorted(items, key=lambda x: x.unit_price, reverse=True)
        remaining_capacity = self.capacity
        total_profit = 0

        for item in sorted_items:
            if item.weight <= remaining_capacity:
                total_profit += item.profit
                remaining_capacity -= item.weight

        return total_profit

def parse_input(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file {file_path} does not exist.")

    items = []
    with open(file_path, 'r') as f:
        capacity = int(f.readline().strip())
        for line in f:
            try:
                weight, profit = map(int, line.split())
                if weight > 0 and profit >= 0:
                    items.append(Item(weight, profit))
            except ValueError:
                continue  # Skip malformed lines
    return capacity, items

def main(input_file="odev", random_iterations=1000000):
    try:
        capacity, items = parse_input(input_file)
        knapsack = Knapsack(capacity)

        greedy_profit = knapsack.greedy_solution(items)
        print(f"The profit of the greedy algorithm: {greedy_profit}")

        min_profit, max_profit, total_profit, better_than_greedy = float('inf'), 0, 0, 0

        for _ in range(random_iterations):
            random_profit = knapsack.random_solution(items)
            total_profit += random_profit
            min_profit = min(min_profit, random_profit)
            max_profit = max(max_profit, random_profit)
            if random_profit > greedy_profit:
                better_than_greedy += 1

        avg_profit = total_profit / random_iterations

        print(f"Stats of the profits of the {random_iterations} random solutions:")
        print(f"Minimum: {min_profit}, Average: {avg_profit:.2f}, Maximum: {max_profit}")
        print(f"Number of times random is better: {better_than_greedy}/{random_iterations}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Knapsack Problem Solver (odev.py)")
    parser.add_argument("input_file", nargs="?", default="test.in", help="Path to the input file containing the knapsack problem instance.")
    parser.add_argument("--random_iterations", type=int, default=10000, help="Number of iterations for random solution testing.")
    args = parser.parse_args()

    main(args.input_file, random_iterations=args.random_iterations)
