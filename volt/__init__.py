# coding: utf-8

__author__ = 'Ryo HIGASHIGAWA'
__version__ = '0.0.1'
__licencse__ = 'MIT'


class RoutingTree(object):
    """URL Routing Tree Structure."""

    def __init__(self, root=None, pos=None):
        """tree structture initialize."""
        if root is None:
            self.root = RoutingTreeNode()
        elif isinstance(root, RoutingTreeNode):
            self.root = root
        else:
            raise
        self.pos = self.root

    def find_node_and_insert(self, key, x, path=[]):
        """find node and insert."""
        self.pos.insert(key, x)

    def move_next_node(self, key):
        """move into tree to next node."""
        self.pos = self.pos[key]


class RoutingTreeNode(object):
    """Tree Node class."""

    def __init__(self, x='', pre_node=None, next_nodes=None):
        """tree node initialize."""
        self.x = x
        self.pre_node = pre_node
        if next_nodes is None:
            self.next_nodes = {}
        elif isinstance(next_nodes, dict):
            self.next_nodes = next_nodes

    def is_root(self):
        """is root?."""
        return self.pre_node is None

    def insert(self, key, node):
        """node insert to next_nodes."""
        if self.next_nodes.get(key, None) is None:
            self.next_nodes[key] = node
        else:
            raise

    def __str__(self):
        return '<RoutingTreeNode: x={}, pre_node={}, next_nodes={}>'.format(self.x, self.pre_node, self.next_nodes)


class Routing(object):
    """URL mapping class."""

    routing_tree = RoutingTree()

    @classmethod
    def add(cls, routings):
        """add a routing."""
        for path, dest in routings:
            names = cls.split(path)
            for key in names:
                cls.routing_tree.pos.insert(key)
                print(cls.routing_tree.pos)
                cls.routing_tree.move_next_node(key)


    @classmethod
    def config(cls):
        """output routing to standard I/O."""
        print(cls._routing)


    @classmethod
    def split(cls, path):
        """split routing path."""
        return path.split('/')[1:]
