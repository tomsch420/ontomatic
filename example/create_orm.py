import os

from ormatic.ormatic import ORMatic
from sqlalchemy import create_engine
from sqlalchemy.orm import registry
import sqlacodegen

import vet_clinic
import sys, inspect

def vet_clinic_classes():
    return [
        getattr(vet_clinic, attr)
        for attr in dir(vet_clinic)
        if isinstance(getattr(vet_clinic, attr), type)
    ]

vet_clinic_orm_path = os.path.join(os.path.dirname(__file__), "orm.py")

def main():
    engine = create_engine("sqlite:///:memory:")

    ormatic = ORMatic(vet_clinic_classes(), registry())
    ormatic.make_all_tables()
    ormatic.mapper_registry.metadata.create_all(engine)
    generator = sqlacodegen.generators.TablesGenerator(ormatic.mapper_registry.metadata, engine, [])

    with open(vet_clinic_orm_path, 'w') as f:
        ormatic.to_python_file(generator, f)

if __name__ == '__main__':
    main()