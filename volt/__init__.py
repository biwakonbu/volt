# coding: utf-8

__author__ = 'Ryo HIGASHIGAWA'
__version__ = '0.0.1'
__licencse__ = 'MIT'

# Routing classes.


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
        self.routing = {}

    def find_node_and_insert(self, key, x, path=[]):
        """find node and insert."""
        self.pos.insert(key, x)

    def move_next_node(self, key):
        """move into tree to next node."""
        self.pos = self.pos.next_nodes[key]

    def return_root(self):
        """move to root node."""
        self.pos = self.root

    def config(self):
        """output routing to standard I/O."""
        sorted_routing = sorted(self.routing.items(), key=lambda x: x[1].__name__)
        max_method_length = max(map(lambda x: len(x[1].__name__), sorted_routing))

        def output(m, r):
            blank = ' ' * (max_method_length - len(m)) + '\t'
            return '{}{}{}'.format(m, blank, r)

        print(output('method', 'routing'))
        print('{}'.format('-' * 60))

        for r, m in sorted_routing:
            print(output(m.__name__, r))


class RoutingTreeNode(object):
    """Tree Node class."""

    def __init__(self, x='', pre_node=None, next_nodes=None):
        """tree node initialize.

        Args:
            x          (function): execute function when the route match.
            pre_node   (RoutingTreeNode): parent node and default None type.
            next_nodes (RoutingTreeNode): children node and default None type.
        """
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
        """node insert to next_nodes.

        Args:
            key  (str): next nodes key.
            node (RoutingTreeNode): next node.
        Todo:
            * change to specific routing duplicate error because raise is generic.
        """
        if self.next_nodes.get(key, None) is None:
            self.next_nodes[key] = node
        else:
            raise

    def __str__(self):
        return '<RoutingTreeNode: x={}, pre_node={}, next_nodes={}>'.format(self.x, self.pre_node, self.next_nodes)


class Routing(object):
    """URL mapping class."""

    tree = RoutingTree()

    @classmethod
    def add(cls, routings):
        """add a routing.

        Args:
            routings (tuple): routing tuples.
                              ('/api/routing/', 'execute_method')
        """
        for path, dest in routings:
            names = cls.split(path)
            for key in names:
                if key and cls.tree.pos.next_nodes.get(key, None) is None:
                    cls.tree.pos.insert(key, RoutingTreeNode('', cls.tree.pos))
                elif key == '':
                    break
                cls.tree.move_next_node(key)
            cls.tree.routing[path] = dest
            cls.tree.pos.x = dest
            cls.tree.return_root()

    @classmethod
    def routing(cls):
        """output routing to standard I/O."""
        cls.tree.config()

    @classmethod
    def match(cls, path):
        """routing match the method execute."""
        names = cls.split(path)
        for key in names:
            if cls.tree.pos.next_nodes.get(key, None):
                cls.tree.move_next_node(key)
        return cls.tree.pos.x()

    @staticmethod
    def split(path):
        """split routing path."""
        return path.split('/')[1:]


# Views

class UndefinedHTTPMethodError(Exception): pass;
class UndefinedGETMethodError(UndefinedHTTPMethodError): pass;
class UndefinedPOSTMethodError(UndefinedHTTPMethodError): pass;

class View(object):

    @classmethod
    def as_view(cls):
        pass

    def get(*args, **kwargs):
        raise UndefinedGETMethodError

    def post(*args, **kwargs):
        raise UndefinedPOSTMethodError


# WSGI application

from wsgiref import simple_server

def server(env, res):
    res('200 OK', [('Content-Type', 'text/plain')])
    return Routing.match(env['PATH_INFO'])

def app():
    wsgi_server = simple_server.make_server('', 5000, server)
    wsgi_server.serve_forever()
