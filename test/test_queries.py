import unittest
import os

from ormatic.ormatic import ORMatic
from owlready2 import get_ontology, Ontology, onto_path

from ontomatic.ontomatic import OntologyDependencyGraph, OntologyQuery

vet_clinic_ontology_path = os.path.join(os.path.dirname(__file__), "..", 'resources', "VetClinic.owl")
vet_clinic_examples_path = os.path.join(os.path.dirname(__file__), "..", 'resources', "VetClinicExamples.owl")

vet_clinic_py_path = os.path.join(os.path.dirname(__file__), "..", "example", "vet_clinic.py")

class QueryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Class-level setup to load ontology from resources using owlready2.
        """
        vet_clinic = get_ontology(f"file://{vet_clinic_ontology_path}").load()
        cls.ontology = get_ontology(f"file://{vet_clinic_examples_path}").load()

    def test_graph(self):
        all_classes = list(self.ontology.classes())
        clazz = list(self.ontology.classes())[2]
        query = OntologyQuery(clazz)
        print(clazz.equivalent_to)
        

if __name__ == '__main__':
    unittest.main()