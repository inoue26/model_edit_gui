# load model. get information and set position of node 
from keras.model import load_model
import pydot


def get_nodes_edges(model):
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
        node = pydot.Node(layer_id, label=label)
        dot.add_node(node)
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
                    assert dot.get_node(inbound_layer_id)
                    assert dot.get_node(layer_id)
                    # graphにedgeを登録
                    dot.add_edge(pydot.Edge(inbound_layer_id, layer_id))
    return dot


def set_position(nodes, edges):
    pass


if __name__ == '__main__':
    model = load_model('./models/model.h5')
