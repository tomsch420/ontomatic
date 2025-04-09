from typing import Type, Union, List

import networkx as nx
from owlready2 import Thing, Ontology
import matplotlib.pyplot as plt


class OntologyDependencyGraph:

    ontology: Ontology
    
    def __init__(self, ontology):
        """
        Initializes the OntologyGraph with a loaded ontology.

        :param ontology: The ontology loaded with owlready2.
        """
        self.ontology = ontology
        self.graph = nx.DiGraph()  # Directed Graph to represent dependencies
        self.build_graph()

    def build_graph(self):
        """
        Builds a dependency graph for the ontology classes based on subclass relationships.
        """

        # Iterate over all classes in the ontology
        for cls in self.ontology.classes():
            # Add the current class as a node
            self.graph.add_node(cls)

            # Add edges for all subclass relationships
            for subclass in cls.subclasses():
                self.graph.add_edge(cls, subclass)

    def class_to_dataclass(self, ontology_class: Type[Thing]):
        """
        Converts a given ontology class to a Python dataclass, including its object and data properties.
    
        :param ontology_class: The class from the ontology.
        :return: A string representation of the Python dataclass.
        """
        class_name = ontology_class.name.capitalize()
        data_properties = {}
        relations = {}
        
        for data_property in self.ontology.data_properties():
            if ontology_class in data_property.domain:
                data_properties[data_property.name] = data_property.range[0].__name__

        # parse object properties
        for object_property in self.ontology.object_properties():
            if ontology_class in object_property.domain:
                relations[object_property.name] = object_property.range


        # Construct the Python dataclass definition
        dataclass_representation = f"@dataclass\nclass {class_name}:\n"
        for prop_name, prop_type in data_properties.items():
            dataclass_representation += f"    {prop_name}: {prop_type} = None\n"

        for relation_name, relation_type in relations.items():
            if len(relation_type) > 1:
                relation_type = f"Union[{', '.join([cls.name for cls in relation_type])}]"
            else:
                relation_type = relation_type[0].__name__
            dataclass_representation += f"    {relation_name}: {relation_type} = None\n"

        return dataclass_representation

    @property
    def roots(self):
        """

        Returns all root nodes of the graph.
        Root nodes are defined as nodes with no incoming edges.
    
        :return: A list of root nodes in the graph.
        """
        return [node for node in self.graph.nodes if self.graph.in_degree(node) == 0]

    def display_graph(self):
        """
        Optionally display the graph using matplotlib.
        Requires: `matplotlib` library.
        """

        pos = nx.drawing.bfs_layout(self.graph, self.roots())
        nx.draw(self.graph, pos, labels={node: node.name for node in self.graph.nodes}, with_labels=True, )
        plt.title("Ontology Dependency Graph")
        plt.show()
