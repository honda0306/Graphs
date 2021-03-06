"""
General drawing methods for graphs using Bokeh.
"""

from random import choice, random
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (GraphRenderer, StaticLayoutProvider, Circle, LabelSet,
                          ColumnDataSource)



class BokehGraph:
    """Class that takes a graph and exposes drawing methods."""
    def __init__(self, graph, title='Bokeh_Graph', width=10, height=10,
                 show_axis=False, show_grid=False, circle_size=35, draw_components=False):
        # Catch error if vertices are not declared
        if not graph.vertices:
            raise Exception('Graph needs vertices in order to render properly!')
        self.graph = graph # Setup plot
        self.title = title
        self.graph = graph
        self.width = width
        self.height = height
        self.pos = {}  # dict to map vertices to x, y positions
        self.plot = figure(title=title, x_range=(0, width), y_range=(0, height))
        self.plot.axis.visible = show_axis
        self.plot.grid.visible = show_grid
        self._setup_graph_renderer(circle_size, draw_components)
        self._setup_labels()

    def _setup_graph_renderer(self, circle_size, draw_components):
        graph_renderer = GraphRenderer()
        self.vertex_keys = list(self.graph.vertices.keys())

        graph_renderer.node_renderer.data_source.add([vertex.label for vertex in self.vertex_keys], 'index')
        colors = (self._get_connected_component_colors() if draw_components
                    else self._get_random_colors())
        graph_renderer.node_renderer.data_source.add(colors, 'color')
        graph_renderer.node_renderer.glyph = Circle(size=circle_size,
                                                    fill_color='color')
        graph_renderer.edge_renderer.data_source.data = self._get_edge_indexes()
        self.randomize()
        graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=self.pos)
        self.plot.renderers.append(graph_renderer)

    def _get_random_colors(self, num_colors=None):
        colors = []
        num_colors = num_colors or len(self.graph.vertices)
        for _ in range(num_colors):
            color = '#'+''.join([choice('0123456789ABCDEF') for j in range(6)])
            colors.append(color)
        return colors

    def _get_edge_indexes(self):
        start_indices = []
        end_indices = []
        checked = set()

        for vertex, edges in self.graph.vertices.items():
            if vertex not in checked:
                for destination in edges:
                    start_indices.append(vertex.label)
                    end_indices.append(destination.label)
                checked.add(vertex)

        return dict(start=start_indices, end=end_indices)

    def _setup_labels(self):
        label_data = {'x': [], 'y': [], 'names': []}
        for vertex, position in self.pos.items():
            label_data['x'].append(position[0])
            label_data['y'].append(position[1])
            label_data['names'].append(str(vertex))
        label_source = ColumnDataSource(label_data)
        labels = LabelSet(x='x', y='y', text='names', level='glyph',
                          text_align='center', text_baseline='middle',
                          source=label_source, render_mode='canvas')
        self.plot.add_layout(labels)

    def show(self, output_path='./graph.html'):
        output_file(output_path)
        show(self.plot)

    def randomize(self):
        """Randomize vertex positions."""
        for vertex in self.vertex_keys:
            # TODO make bounds and random draws less hacky
            self.pos[vertex.label] = (1 + random() * (self.width - 2),
                                1 + random() * (self.height - 2))

    def _get_connected_component_colors(self):
        self.graph.find_components()
        component_colors = self._get_random_colors(self.graph.components)
        vertex_colors = []
        for vertex in self.vertex_keys:
            vertex_colors.append(component_colors[vertex.component])
        return vertex_colors

from graph import Graph
from draw import BokehGraph

# graph = Graph()
# graph.create_vertex(0)
# graph.create_vertex(1)
# graph.create_vertex(2)
# graph.create_vertex(3)
# graph.create_vertex(4)
# graph.create_edge(0, 1)
# graph.create_edge(1, 2)
# graph.create_edge(2, 3)


# graph.vertices

# bokeh_graph = BokehGraph(graph)
# dir(bokeh_graph)
# bokeh_graph.pos
# bokeh_graph.plot
# bokeh_graph.show()