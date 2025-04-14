from __future__ import annotations

from dataclasses import dataclass
from typing import Type, Union, List, Dict, Optional

import networkx as nx
from owlready2 import Thing, Ontology
import matplotlib.pyplot as plt


@dataclass
class OntologyClass:
    name: str
    owl_class: Type[Thing]
    super_class: Optional[OntologyClass]
    data_properties: Dict[str, type]

    def as_dataclass(self) -> str:
        """
        Converts the OntologyClass instance into a Python dataclass string format.

        :return: A string representation of a dataclass with the attributes of this class.
        """
        if self.super_class:
            dataclass_representation = f"@dataclass\nclass {self.name}({self.super_class.name}):\n"
        else:
            dataclass_representation = f"@dataclass\nclass {self.name}:\n"
        if not self.data_properties:
            dataclass_representation += "    ...\n"
        for prop_name, prop_type in self.data_properties.items():
            dataclass_representation += f"    {prop_name}: {prop_type.__name__}\n"
        return dataclass_representation


@dataclass
class OntologyRelation:
    name: str
    owl_relation: Type[Thing]

    left: str
    right: str

    def as_dataclass(self) -> str:
        return f"@dataclass\nclass {self.name}:\n    left: {self.left}\n    right: {self.right}"

@dataclass
class OntologyQuery:
    """
    Class to represent an ontology query that is expressed by an ontological concept.
    """
    restriction: Type[Thing]

    def to_sql(self):
        print(self.restriction)



class OntologyDependencyGraph:

    ontology: Ontology
    class_dependency_graph: nx.DiGraph
    relation_dependency_graph: nx.DiGraph

    classes: Dict[Type[Thing], OntologyClass]
    relations: Dict[Type[Thing], OntologyRelation]
    
    def __init__(self, ontology):
        """
        Initializes the OntologyGraph with a loaded ontology.

        :param ontology: The ontology loaded with owlready2.
        """
        self.ontology = ontology
        self.class_dependency_graph = nx.DiGraph()
        self.relation_dependency_graph = nx.DiGraph()
        self.build_class_dependency_graph()
        self.build_relation_dependency_graph()
        self.classes = {}
        self.relations = {}


    def build_class_dependency_graph(self):
        """
        Builds a dependency graph for the ontology classes based on subclass relationships.
        """

        # Iterate over all classes in the ontology
        for cls in self.ontology.classes():
            # Add the current class as a node
            self.class_dependency_graph.add_node(cls)

            # Add edges for all subclass relationships
            for subclass in cls.subclasses():
                self.class_dependency_graph.add_edge(cls, subclass)

    def build_relation_dependency_graph(self):
        # Iterate over all classes in the ontology
        for cls in self.ontology.object_properties():
            # Add the current class as a node
            self.relation_dependency_graph.add_node(cls)

            # Add edges for all subclass relationships
            for subclass in cls.subclasses():
                self.relation_dependency_graph.add_edge(cls, subclass)

    def create_ontology_classes(self):
        for cls in nx.topological_sort(self.class_dependency_graph):
            self.classes[cls] = self.class_to_dataclass(cls)

    def create_relations(self):
        for relation in nx.topological_sort(self.relation_dependency_graph):
            self.relations[relation] = self.object_property_to_relation(relation)

    def object_property_to_relation(self, object_property: Type[Thing]) -> Union:
        return OntologyRelation(object_property.name, object_property, object_property.domain[0].__name__, object_property.range[0].__name__)

    def class_to_dataclass(self, ontology_class: Type[Thing]) -> OntologyClass:
        """
        Converts a given ontology class to a Python dataclass, including its object and data properties.
    
        :param ontology_class: The class from the ontology.
        :return: A string representation of the Python dataclass.
        """
        class_name = ontology_class.name
        data_properties = {}
        super_classes = [parent for parent, child in self.class_dependency_graph.in_edges(ontology_class)]
        if super_classes:
            super_class = super_classes[0]
        else:
            super_class = None
        for data_property in self.ontology.data_properties():
            if ontology_class in data_property.domain:
                data_properties[data_property.name] = data_property.range[0]

        return OntologyClass(class_name, ontology_class, super_class, data_properties)

    @property
    def roots(self):
        """
        :return: A list of root nodes in the graph.
        """
        return [node for node in self.class_dependency_graph.nodes if self.class_dependency_graph.in_degree(node) == 0]

    def display_graph(self):
        """
        Optionally display the graph using matplotlib.
        Requires: `matplotlib` library.
        """

        pos = nx.drawing.bfs_layout(self.class_dependency_graph, self.roots())
        nx.draw(self.class_dependency_graph, pos, labels={node: node.name for node in self.class_dependency_graph.nodes}, with_labels=True, )
        plt.title("Ontology Dependency Graph")
        plt.show()

    def to_python_file(self, file_path: str):
        """
        Exports all ontology classes and relations to a Python file as dataclasses.
        
        :param file_path: The path to the file where the Python code will be exported.
        """
        with open(file_path, 'w') as file:
            # Write header
            file.write("from dataclasses import dataclass\n\n")

            # Write all ontology classes
            for ontology_class in self.classes.values():
                file.write(ontology_class.as_dataclass() + "\n\n")

            # Write all ontology relations
            for ontology_relation in self.relations.values():
                file.write(ontology_relation.as_dataclass() + "\n\n")
