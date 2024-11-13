class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.ratio = value / weight
    def knapsack(items, capacity):
        items.sort(key=lambda x: x.ratio, reverse=True)
        n = len(items)
        curr_weight = 0
        curr_value = 0
        max_value = 0
        solution = [0] * n
        stack = []

        node = Node(0, 0, 0, 0, solution[:])
        stack.append(node)
        while stack:
            node = stack.pop()
            level = node.level
            curr_weight = node.weight
            curr_value = node.value

        if level == n or curr_weight == capacity:
            if curr_value > max_value:
                max_value = curr_value
                solution = node.solution
            continue
 
        if curr_weight + items[level].weight <= capacity:
            new_solution = node.solution[:]
            new_solution[level] = 1
            stack.append(Node(level + 1, curr_weight +items[level].weight,curr_value + items[level].value, node.bound,new_solution))

        bound = node.bound
        if level < n - 1:
            bound += (capacity - curr_weight) * items[level + 1].ratio
 
        if bound > max_value:
            stack.append(Node(level + 1, curr_weight, curr_value, bound,
node.solution))
        return max_value, solution
    
class Node:
 def __init__(self, level, weight, value, bound, solution):
     self.level = level
     self.weight = weight
     self.value = value
     self.bound = bound
     self.solution = solution

items = []
n = int(input("Enter the number of items: "))
for i in range(n):
 weight = int(input(f"Enter the weight of item {i + 1}: "))
 value = int(input(f"Enter the value of item {i + 1}: "))
 items.append(Item(weight, value))
capacity = int(input("Enter the capacity of the knapsack: "))
# Solve the knapsack problem
max_value, solution = Item.knapsack(items, capacity)
# Print the result
print("Max Value:", max_value)
print("Solution:", solution)