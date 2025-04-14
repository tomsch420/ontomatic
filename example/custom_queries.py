from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from vet_clinic import *
from orm import *


bodiless_animal = select(Animal).join(hasPart)


def main():
    engine = create_engine("sqlite:///:memory:")
    session = Session(engine)
    metadata.create_all(engine)

    cat_1 = Cat(2.)
    body_part_1 = BiologicalObject(1)
    cb_1 = hasPart(cat_1, body_part_1)
    session.add(cb_1)
    session.commit()

    result = session.scalars(bodiless_animal).all()




if __name__ == '__main__':
    main()