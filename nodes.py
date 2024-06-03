class MNode:
    def __init__(self, m):
        self.m = m
        self.keys = []
        self.children = []

    def insert(self, key):
        if not self.children:
            self.keys.append(key)
            self.keys.sort()
            if len(self.keys) >= self.m:
                return self.split()
        else:
            for i, item in enumerate(self.keys):
                if key < item:
                    res = self.children[i].insert(key)
                    if res:
                        return self.handle_split(res, i)
                    return None
            res = self.children[-1].insert(key)
            if res:
                return self.handle_split(res, len(self.keys))
        return None

    def split(self):
        mid_index = len(self.keys) // 2
        mid_value = self.keys[mid_index]

        left_child = MNode(self.m)
        right_child = MNode(self.m)
        
        left_child.keys = self.keys[:mid_index]
        right_child.keys = self.keys[mid_index+1:]

        if self.children:
            left_child.children = self.children[:mid_index + 1]
            right_child.children = self.children[mid_index + 1:]

        return mid_value, left_child, right_child

    def handle_split(self, split_data, index):
        mid_value, left_child, right_child = split_data

        self.keys.insert(index, mid_value)
        self.children[index] = left_child
        self.children.insert(index + 1, right_child)

        if len(self.keys) >= self.m:
            return self.split()
        return None

    def print_tree(self, depth=0, child_type='root'):
        result = " " * (4 * depth) + f"{child_type.upper()} {self.keys}\n"
        for i, child in enumerate(self.children):
            child_type = 'left' if i == 0 else 'right' if i == len(self.children) - 1 else 'middle'
            result += child.print_tree(depth + 1, child_type)
        return result

    def search(self, key, level=0):
        for i, item in enumerate(self.keys):
            if key == item:
                return f"Found {key} at level {level}"
            elif key < item:
                if self.children:
                    return self.children[i].search(key, level + 1)
                return None
        if self.children:
            return self.children[-1].search(key, level + 1)
        return None

class MSearchTree:
    def __init__(self, m):
        self.root = MNode(m)

    def search(self, key):
        return self.root.search(key)
