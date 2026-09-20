import networkx as nx


class KnowledgeGraph:

    def __init__(self):

        self.graph = nx.DiGraph()

    def add_node(self, identifier, **meta):

        self.graph.add_node(identifier, **meta)

    def relate(self, parent, child, relation):

        self.graph.add_edge(

            parent,

            child,

            relationship=relation

        )
