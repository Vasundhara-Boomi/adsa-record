class BPlusTree:
    def __init__(self, order):
        self.order = order
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = BPlusTreeNode(self.order, is_leaf=True)
        if self.root.is_full():
            old_root = self.root
            self.root = BPlusTreeNode(self.order)
            self.root.children.append(old_root)
            self.root.split_child(0)

        self.root.insert_non_full(key, value)

    def delete(self, key):
        if self.root is None:
            return

        self.root.delete(key)
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]

    def print_tree(self):
        self.root.print_node()
    def search(self, key):
        if self.root is None:
            print("Tree is empty.")
            return

        result = self.root.search(key)
        if result:
            print(f"Key {key} found:")
        else:
            print(f"Key {key} not found.")

class BPlusTreeNode:
    def __init__(self, order, is_leaf=False):
        self.order = order
        self.keys = []
        self.values = []
        self.children = []
        self.is_leaf = is_leaf

    def is_full(self):
        return len(self.keys) == self.order - 1

    def insert_non_full(self, key, value):
        if self.is_leaf:
            self.insert_into_leaf(key, value)
        else:
            index = self.find_child_index(key)
            if self.children[index].is_full():
                self.split_child(index)
                if key > self.keys[index]:
                    index += 1
            self.children[index].insert_non_full(key, value)

    def insert_into_leaf(self, key, value):
        index = 0
        while index < len(self.keys) and key > self.keys[index]:
            index += 1
        self.keys.insert(index, key)
        self.values.insert(index, value)

    def split_child(self, child_index):
        child = self.children[child_index]
        new_child = BPlusTreeNode(self.order, is_leaf=child.is_leaf)
        mid_index = self.order // 2

        self.keys.insert(child_index, child.keys[mid_index])
        self.values.insert(child_index, child.values[mid_index])
        self.children.insert(child_index + 1, new_child)

        new_child.keys = child.keys[mid_index:]
        new_child.values = child.values[mid_index:]
        child.keys = child.keys[:mid_index]
        child.values = child.values[:mid_index]

    def find_child_index(self, key):
        index = 0
        while index < len(self.keys) and key > self.keys[index]:
            index += 1
        return index

    def delete(self, key):
        if self.is_leaf:
            self.delete_from_leaf(key)
        else:
            index = self.find_child_index(key)
            if index < len(self.keys) and key == self.keys[index]:
                predecessor = self.children[index].get_max_key()
                self.keys[index] = predecessor
                self.children[index].delete(predecessor)
            else:
                self.children[index].delete(key)

            if len(self.children[index].keys) < (self.order - 1) // 2:
                self.fix_child_underflow(index)

    def delete_from_leaf(self, key):
        index = 0
        while index < len(self.keys) and key > self.keys[index]:
            index += 1

        if index < len(self.keys) and key == self.keys[index]:
            self.keys.pop(index)
            self.values.pop(index)

    def get_max_key(self):
        if self.is_leaf:
            return self.keys[-1]
        else:
            return self.children[-1].get_max_key()
    def fix_child_underflow(self, child_index):
        if child_index > 0 and len(self.children[child_index - 1].keys) > (self.order - 1) // 2:
            self.borrow_from_previous(child_index)
        elif child_index < len(self.children) - 1 and len(self.children[child_index + 1].keys) > (self.order - 1) // 2:
            self.borrow_from_next(child_index)
        elif child_index > 0:
            self.merge_with_previous(child_index)
        else:
            self.merge_with_next(child_index)

    def borrow_from_previous(self, child_index):
        child = self.children[child_index]
        sibling = self.children[child_index - 1]

        child.keys.insert(0, self.keys[child_index - 1])
        child.values.insert(0, sibling.values.pop())
        self.keys[child_index - 1] = sibling.keys.pop()

        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_next(self, child_index):
        child = self.children[child_index]
        sibling = self.children[child_index + 1]

        child.keys.append(self.keys[child_index])
        child.values.append(sibling.values.pop(0))
        self.keys[child_index] = sibling.keys.pop(0)

        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))

    def merge_with_previous(self, child_index):
        child = self.children[child_index]
        sibling = self.children[child_index - 1]

        sibling.keys.append(self.keys[child_index - 1])
        sibling.values.extend(child.values)
        self.keys.pop(child_index - 1)
        self.children.pop(child_index)

        if not child.is_leaf:
            sibling.children.extend(child.children)

    def merge_with_next(self, child_index):
        child = self.children[child_index]
        sibling = self.children[child_index + 1]

        child.keys.append(self.keys[child_index])
        child.values.extend(sibling.values)
        self.keys.pop(child_index)
        self.children.pop(child_index + 1)

        if not child.is_leaf:
            child.children.extend(sibling.children)

    def print_node(self, level=0):
        if self.is_leaf:
            print(f"Level {level}: {self.keys}")
        else:
            print(f"Level {level}: {self.keys}")
            for child in self.children:
                child.print_node(level + 1)
    def search(self, key):
        index = self.find_child_index(key)
        if index < len(self.keys) and key == self.keys[index]:
            return self.values[index]
        elif self.is_leaf:
            return None
        else:
            return self.children[index].search(key)

#Driver Code

if __name__ == '__main__':
    order=int(input("Enter the order of b plus tree:"))
    b_plus_tree = BPlusTree(order)

    while True:
        ch=int(input("[1:Insert,2:Delete,3:Display,4:Exit,5:Search]\nEnter the choice:"))
        if ch == 1:
            n=int(input("Enter number of values to be inserted:"))
            for _ in range(n):
                value=int(input("Enter the value:"))
                b_plus_tree.insert(value, f'Value {value}')
            print(f"After inserting:")
            b_plus_tree.print_tree()
            print()
        elif ch == 2 :
            value=int(input("Enter value to be deleted:"))
            b_plus_tree.delete(value)
            print(f"After deleting:")
            b_plus_tree.print_tree()
            print()
        elif ch == 3:
            print("Final Tree Structure:")
            b_plus_tree.print_tree()
        elif ch == 4:
            print("Exiting..")
            break
        elif ch == 5:
            value=int(input("Enter key to be serched:"))
            b_plus_tree.search(value)
        else:
            print("Invalid choice")