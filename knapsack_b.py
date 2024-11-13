class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.ratio = value / weight

def knapsack_branch_and_bound(items, capacity):
    items.sort(key=lambda x: x.ratio, reverse=True)  # Sort items by value-to-weight ratio in descending order
    n = len(items)

    # Helper function to calculate the upper bound of a node
    def upper_bound(level, weight, value):
        if weight >= capacity:
            return 0
        upper_bound_value = value
        j = level + 1
        total_weight = weight
        while j < n and total_weight + items[j].weight <= capacity:
            total_weight += items[j].weight
            upper_bound_value += items[j].value
            j += 1
        if j < n:
            remaining_capacity = capacity - total_weight
            upper_bound_value += items[j].ratio * remaining_capacity  # Corrected line
        return upper_bound_value

    max_value = 0
    best_items = []

    stack = [(0, 0, 0, [])]  # (level, weight, value, chosen_items)

    while stack:
        level, weight, value, chosen_items = stack.pop()
        if level >= n:
            if value > max_value:
                max_value = value
                best_items = chosen_items
        else:
            if weight + items[level].weight <= capacity:
                new_weight = weight + items[level].weight
                new_value = value + items[level].value
                new_chosen_items = chosen_items + [items[level]]
                stack.append((level + 1, new_weight, new_value, new_chosen_items))

            if upper_bound(level, weight, value) > max_value:
                stack.append((level + 1, weight, value, chosen_items))

    return max_value, best_items


# User input
n = int(input("Enter the number of items: "))
items = []
for i in range(n):
    value = int(input(f"Enter the value of item {i+1}: "))
    weight = int(input(f"Enter the weight of item {i+1}: "))
    items.append(Item(weight, value))
capacity = int(input("Enter the capacity of the knapsack: "))

# Solve the knapsack problem using Branch and Bound
max_value, best_items = knapsack_branch_and_bound(items, capacity)

# Print the result
print("Optimal Solution:")
print("Maximum Value:", max_value)
print("Selected Items:")
for item in best_items:
    print("Weight:", item.weight, "Value:", item.value)
