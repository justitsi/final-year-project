num_nodes = 12
num_groups = 6

num_ops = 0

for i in range(1, num_nodes):
    num_ops += pow(num_groups, i)

print(f'Nodes: {num_nodes}, Groups: {num_groups}')
print("Number of solutions:")
print(pow(num_groups, (num_nodes-1)))
print("Number of operations:")
print(num_ops)
