def knapsack_approximation(values, weights, capacity):
    n = len(values)
    items = list(range(n))
    ratios = [(values[i] / weights[i], i) for i in range(n)]
    ratios.sort(reverse=True)
    
    total_value = 0
    total_weight = 0
    selected_items = []
    
    for ratio, i in ratios:
        if total_weight + weights[i] <= capacity:
            total_value += values[i]
            total_weight += weights[i]
            selected_items.append(i)
    
    return total_value, selected_items

# User input
n = int(input("Enter the number of items: "))
values = []
weights = []
for i in range(n):
    value = int(input("Enter the value of item {}: ".format(i+1)))
    weight = int(input("Enter the weight of item {}: ".format(i+1)))
    values.append(value)
    weights.append(weight)
capacity = int(input("Enter the capacity of the knapsack: "))

total_value, selected_items = knapsack_approximation(values, weights, capacity)

print("Selected items:", selected_items)
print("Total value:", total_value)  