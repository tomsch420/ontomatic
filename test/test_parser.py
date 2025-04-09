import unittest
import os
from owlready2 import get_ontology, Ontology

from ontomatic.ontomatic import OntologyDependencyGraph


class ParserTestCase(unittest.TestCase):

    ontology: Ontology

    @classmethod
    def setUpClass(cls):
        """
        Class-level setup to load ontology from resources using owlready2.
        """
        # Define the path to the ontology file in the resources folder
        resources_path = os.path.join(os.path.dirname(__file__), "..", 'resources')
        ontology_file = os.path.join(resources_path, 'VetClinic.owl')  # Replace with your actual ontology filename

        # Use `owlready2` to load the ontology
        cls.ontology = get_ontology(f"file://{ontology_file}").load()

    def test_graph(self):
        all_classes = list(self.ontology.classes())
        dependency_graph = OntologyDependencyGraph(self.ontology)
        # dependency_graph.display_graph()

        print(dependency_graph.class_to_dataclass(all_classes[2]))

if __name__ == '__main__':
    unittest.main()