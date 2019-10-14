import networkx as nx
import matplotlib.pyplot as plt
import numpy
import numpy as np
import pylab
import time


def refreshGraph():
    plt.close()
    fig=plt.figure()
    ax=fig.add_subplot(111)
    fig.canvas.mpl_connect('button_press_event', onClick)
    # print('blue', blue)
    nx.draw_networkx_nodes(T, pos,
                       nodelist=red,
                       node_color='r',
                       alpha=0.8)
    nx.draw_networkx_nodes(T, pos,
                       nodelist=blue,
                       node_color='b',
                       alpha=0.8)
    nx.draw_networkx_edges(T, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(T, pos, labels, font_size=16)
    plt.axis('off')
    plt.axis((-4,4,-1,3))
    fig.patch.set_facecolor('white')
    plt.show()

    

def onclick(event):
    print('event.button=%d,  event.x=%d, event.y=%d, event.xdata=%f, \
    event.ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata))


def onClick(event):
    (x,y)   = (event.xdata, event.ydata)

    for i in allNodes:            
        node = pos[i]
        distance = pow(x-node[0],2)+pow(y-node[1],2)
        if distance < 0.01:
            print('This node is ', labels[i])
            global blue, red
            """
            try: 
                if i in blue:
                    blue.remove(i)
                    red.append(i)
                elif i in red:
                    red.remove(i)
                    blue.append(i)
                else:
                    raise ValueError("This node belongs neither blue nor red!")
            except ValueError as e:
                print(e)
            """
            if i in blue:
                blue.remove(i)
                red.append(i)
            elif i in red:
                red.remove(i)
                blue.append(i)
            # print('blue', blue)
            refreshGraph()


fig=plt.figure()
ax=fig.add_subplot(111)
fig.canvas.mpl_connect('button_press_event', onClick)

T = nx.Graph()
### Nodes
blue, red = [1, 4, 5, 6, 7], [2, 3]
allNodes = blue + red

for node in allNodes:      
    T.add_node(node)

### Edges
T.add_edge(1, 2)
T.add_edge(1, 3)
T.add_edge(2, 4)
T.add_edge(2, 5)
T.add_edge(3, 6)
T.add_edge(3, 7)

### Positions of the nodes
pos={}
pos[1]=numpy.array([ 0,0])
pos[2]=numpy.array([-2,1])
pos[3]=numpy.array([ 2,1])
pos[4]=numpy.array([-3,2])
pos[5]=numpy.array([-1,2])
pos[6]=numpy.array([ 1,2])
pos[7]=numpy.array([ 3,2])

### labels
labels = {}
labels[1] = '$b$'
labels[2] = '$c$'
labels[3] = '$d$'
labels[4] = '$\\alpha$'
labels[5] = '$\\beta$'
labels[6] = '$\\gamma$'
labels[7] = '$\\delta$'

### Draw nodes and edges
refreshGraph()

