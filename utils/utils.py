import numpy as np
from keras.layers.wrappers import Wrapper
import networkx as nx


class MyNode:
    def __init__(self, id=0, attribute=''):
        self.id = id
        # もしかしたらattributeは辞書形式にしてparseするかも
        self.attribute = attribute
        self.pos = None

    def get_id(self):
        ret = self.id
        return ret

    def get_attribute(self):
        return self.attribute

    def get_name_and_attribute(self):
        ret = 'Node object id:' + str(self.id) + '||' + self.attribute
        return ret

    def set_pos(self, x, y):
        self.pos = np.array([x, y])

    def get_pos(self):
        return self.pos


class MyEdge:
    def __init__(self, src=0, dst=1):
        """[summary]
        Args:
            src (str, id): keras Node Object id of Backward node.
            dst (str, id): keras Node object id of Foeward node.
        """
        self.edge = (src, dst)
        self.src = src
        self.dst = dst

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst
    
    def get_edge(self):
        return self.edge


class MyGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.id_node_map = {}

    def add_node(self, node):
        """add Node object to Graph

        Args:
            node (MyNode class): 
        """
        self.nodes.append(node)
        self.id_node_map[node.get_id()] = node

    def add_edge(self, edge):
        """[summary]
        Args:
            edge (MyEdge class): 
        """
        self.edges.append(edge)

    def get_nodes_id_list(self):
        node_list = []
        for node in self.nodes:
            node_id = node.get_id()
            node_list.append(node_id)

        return node_list

    def get_nodes_attribute_dict(self):
        labels = {}
        for node in self.nodes:
            labels[node.get_id()] = node.get_attribute()

        return labels

    def get_edges_id_list(self):
        edges_list = []
        for edge in self.edges:
            edges_list.append(edge.get_edge())
        return edges_list

    def get_pos_dict(self):
        pos = {}
        for node in self.nodes:
            pos[node.get_id()] = node.get_pos()

        return pos

    def get_node_by_id(self, id_):
        return self.id_node_map[id_]


def get_nodes_edges(model, show_layer_names=True):
    G = MyGraph()

    sub_n_first_node = {}
    sub_n_last_node = {}
    sub_w_first_node = {}
    sub_w_last_node = {}

    layers = model._layers
    # Create graph nodes.
    for i, layer in enumerate(layers):
        layer_id = str(id(layer))
        # Append a wrapped layer's label to node's label, if it exists.
        # ignore model in model.
        layer_name = layer.name
        class_name = layer.__class__.__name__
        if isinstance(layer, Wrapper):
            layer_name = '{}({})'.format(layer_name, layer.layer.name)
            child_class_name = layer.layer.__class__.__name__
            class_name = '{}({})'.format(class_name, child_class_name)

        # Create node's label.
        if show_layer_names:
            label = '{}: {}'.format(layer_name, class_name)
        else:
            label = class_name
        try:
            outputlabels = str(layer.output_shape)
        except AttributeError:
            outputlabels = 'multiple'
        if hasattr(layer, 'input_shape'):
            inputlabels = str(layer.input_shape)
        elif hasattr(layer, 'input_shapes'):
            inputlabels = ', '.join(
                (str(ishape) for ishape in layer.input_shapes))
        else:
            inputlabels = 'multiple'
        label = '%s\n|{input:|output:}|{{%s}|{%s}}' % (label,
                                                       inputlabels,
                                                       outputlabels)
        node = MyNode(layer_id, label)
        G.add_node(node)
    for layer in layers:
        # objectの持つ番号を取得
        layer_id = str(id(layer))
        for i, node in enumerate(layer._inbound_nodes):
            # layerが持つnodeに対しても以下のformatで名前がついている
            node_key = layer.name + '_ib-' + str(i)
            if node_key in model._network_nodes:
                for inbound_layer in node.inbound_layers:
                    inbound_layer_id = str(id(inbound_layer))
                    # graphにinbound_layerが登録されているか確認
                    assert G.get_node_by_id(inbound_layer_id)
                    assert G.get_node_by_id(layer_id)
                    # graphにedgeを登録
                    G.add_edge(MyEdge(inbound_layer_id, layer_id))
    return G


def mygraph2nxgraph(mygraph):
    T = nx.Graph()
    for node in mygraph.get_nodes_id_list():
        T.add_node(node)
    for edge in mygraph.get_edges_id_list():
        T.add_edge(edge[0], edge[1])

    return T
