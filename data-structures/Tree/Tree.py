from itertools import chain

class Node:
    def __init__(self,
                 value: any = None,
                 parent: 'Node' = None,
                 children: list = None):

        self._value = value
        self._parent = parent
        self._children = children if children else []

    def __getitem__(self, item):
        if type(item) == int:
            return self.slice(item, item + 1)
        if type(item) == slice:
            return self.slice(item.start, item.stop)
        raise TypeError

    def add_child(self, child: 'Node'):
        self.children.append(child)
        print(f'Appending child @{self}: {child}\nChildren: {self.children}')

    def add_new_child(self, value=None, children: list = None):
        self.add_child(Node(value, self, children))

    @property
    def children(self):
        return self._children

    @property
    def degree(self):
        return len(self._children)

    @property
    def degree_of_tree(self):
        if self.is_root:
            return max([child.degree for child in self.children] + [self.degree])
        return self.root.degree_of_tree

    @property
    def depth(self):
        return self.level

    @property
    def height(self):
        return 0 if self.is_leaf else max([child.height for child in self.children]) + 1

    def insert_child(self, index: int, child: 'Node'):
        self.children.insert(index, child)

    def insert_new_child(self, index: int, value: any = None, children: list = None):
        self.insert_child(index, Node(value, self, children))

    def is_ancestor_of(self, node: 'Node'):
        return node.is_descendant_of(self)

    def is_child_of(self, node):
        return self.parent is node

    def is_descendant_of(self, node: 'Node'):
        if self.is_root:
            return False
        if self.is_child_of(node):
            return True
        return self.parent.is_descendant_of(node)

    @property
    def is_leaf(self):
        return not self._children

    def is_parent_of(self, node):
        return node.parent is self

    @property
    def is_root(self):
        return self._parent is None

    @property
    def leaves(self):
        return [self] if self.is_leaf else list(chain.from_iterable([child.leaves for child in self.children]))

    @property
    def level(self):
        return 0 if self.is_root else self.parent.level + 1

    @property
    def neighbours(self):
        return ([] if self.is_root else [self.parent]) + self.children

    @property
    def parent(self):
        return self._parent

    @property
    def root(self):
        return self if self.is_root else self.parent.root

    def slice(self, level: int = None):
        level = (level + self.tree_height) % self.tree_height
        level = self.level if level is None else level
        if self.is_root:
            current_level = 0
            current_slice = [self]
            while current_level < level:
                current_slice = list(chain.from_iterable([node.children for node in current_slice]))
                current_level += 1
            return current_slice
        return self.root.slice(level)

    def slices(self, start: int = None, stop: int = None):
        if self.is_root:
            if start is None:
                if stop is None:
                    raise ValueError
                start = 0
            if stop is None:
                stop = self.height
            start = (start + self.tree_height) % self.tree_height
            stop = (stop + self.tree_height) % self.tree_height
            if stop < start:
                raise ValueError
            current_level = start
            current_slice = self.slice(start)
            slices = []
            while current_level < stop:
                current_slice = list(chain.from_iterable([node.children for node in current_slice]))
                slices.append(current_slice)
                current_level += 1
            return slices
        return self.root.slices(start, stop)

    @property
    def tree_height(self):
        return self.root.height

    def width(self, level: int = None):
        level = self.level if level is None else level
        return self.slice(level)
