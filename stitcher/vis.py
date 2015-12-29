
"""
Visualize possible stitches with the outcome of the validator.
"""

import matplotlib.pyplot as plt
import networkx as nx

# TODO: auto scale subplots


def show(graphs, new_nodes, results, prog='neato', size=(2, 4)):
    """
    Display the results using matplotlib.
    """
    fig, axarr = plt.subplots(size[0], size[1], figsize=(18, 10))
    fig.set_facecolor('white')
    x_val = 0
    y_val = 0
    index = 0
    for candidate in graphs:
        # axarr[x_val, y_val].axis('off')
        axarr[x_val, y_val].xaxis.set_major_formatter(plt.NullFormatter())
        axarr[x_val, y_val].yaxis.set_major_formatter(plt.NullFormatter())
        axarr[x_val, y_val].xaxis.set_ticks([])
        axarr[x_val, y_val].yaxis.set_ticks([])
        axarr[x_val, y_val].set_title(results[index])
        axarr[x_val, y_val].set_axis_bgcolor("white")
        _plot_sub_plot(candidate, new_nodes, prog, axarr[x_val, y_val])
        y_val += 1
        if y_val > 3:
            y_val = 0
            x_val += 1
        index += 1
    fig.tight_layout()
    plt.show()


def _plot_sub_plot(graph, new_nodes, prog, axes):
    """
    Plot a single candidate graph.
    """
    pos = nx.graphviz_layout(graph, prog=prog)

    green_nodes = []
    yellow_nodes = []
    red_nodes = []
    blue_nodes = []
    for node, values in graph.nodes(data=True):
        shape = 'o'
        if values['type'] == 'a':
            shape = '^'
        if values['type'] == 'b':
            shape = 's'
        if values['type'] == 'c':
            shape = 'v'
        color = 'g'
        alpha = 0.8
        if node in new_nodes:
            color = 'b'
            alpha = 0.2
        elif 'rank' in values and values['rank'] > 7:
            color = 'r'
        elif 'rank' in values and values['rank'] < 7 and values['rank'] > 3:
            color = 'y'
        nx.draw_networkx_nodes(graph, pos, nodelist=[node], node_color=color,
                               node_shape=shape, alpha=alpha, ax=axes)

        if node in new_nodes:
            blue_nodes.append(node)
        elif 'rank' in values and values['rank'] > 7:
            red_nodes.append(node)
        elif 'rank' in values and values['rank'] < 7 and values['rank'] > 3:
            yellow_nodes.append(node)
        else:
            green_nodes.append(node)

    # draw the edges
    dotted_line = []
    normal_line = []
    for src, trg in graph.edges():
        if src in new_nodes and trg not in new_nodes:
            dotted_line.append((src, trg))
        else:
            normal_line.append((src, trg))
    nx.draw_networkx_edges(graph, pos, edgelist=dotted_line, style='dotted',
                           ax=axes)
    nx.draw_networkx_edges(graph, pos, edgelist=normal_line, ax=axes)

    # draw labels
    nx.draw_networkx_labels(graph, pos, ax=axes)
