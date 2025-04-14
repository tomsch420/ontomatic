from sqlalchemy import Column, Float, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import registry, relationship
import vet_clinic

metadata = MetaData()


t_MedicalCondition = Table(
    'MedicalCondition', metadata,
    Column('id', Integer, primary_key=True),
    Column('polymorphic_type', String)
)

t_Object = Table(
    'Object', metadata,
    Column('id', Integer, primary_key=True),
    Column('hasMass', Float, nullable=False),
    Column('polymorphic_type', String)
)

t_BiologicalObject = Table(
    'BiologicalObject', metadata,
    Column('id', ForeignKey('Object.id'), primary_key=True)
)

t_Injury = Table(
    'Injury', metadata,
    Column('id', ForeignKey('MedicalCondition.id'), primary_key=True)
)

t_hasPart = Table(
    'hasPart', metadata,
    Column('id', Integer, primary_key=True),
    Column('left_id', ForeignKey('Object.id')),
    Column('right_id', ForeignKey('Object.id'))
)

t_Animal = Table(
    'Animal', metadata,
    Column('id', ForeignKey('BiologicalObject.id'), primary_key=True)
)

t_BodyPart = Table(
    'BodyPart', metadata,
    Column('id', ForeignKey('BiologicalObject.id'), primary_key=True)
)

t_BrokenWing = Table(
    'BrokenWing', metadata,
    Column('id', ForeignKey('Injury.id'), primary_key=True)
)

t_affects = Table(
    'affects', metadata,
    Column('id', Integer, primary_key=True),
    Column('left_id', ForeignKey('MedicalCondition.id')),
    Column('right_id', ForeignKey('BiologicalObject.id'))
)

t_Bird = Table(
    'Bird', metadata,
    Column('id', ForeignKey('Animal.id'), primary_key=True)
)

t_Mammal = Table(
    'Mammal', metadata,
    Column('id', ForeignKey('Animal.id'), primary_key=True)
)

t_Reptile = Table(
    'Reptile', metadata,
    Column('id', ForeignKey('Animal.id'), primary_key=True)
)

t_Wing = Table(
    'Wing', metadata,
    Column('id', ForeignKey('BodyPart.id'), primary_key=True)
)

t_suffersFrom = Table(
    'suffersFrom', metadata,
    Column('id', Integer, primary_key=True),
    Column('left_id', ForeignKey('Animal.id')),
    Column('right_id', ForeignKey('MedicalCondition.id'))
)

t_Canary = Table(
    'Canary', metadata,
    Column('id', ForeignKey('Bird.id'), primary_key=True)
)

t_Cat = Table(
    'Cat', metadata,
    Column('id', ForeignKey('Mammal.id'), primary_key=True)
)

t_Dog = Table(
    'Dog', metadata,
    Column('id', ForeignKey('Mammal.id'), primary_key=True)
)

mapper_registry = registry(metadata=metadata)

m_Object = mapper_registry.map_imperatively(vet_clinic.Object, t_Object, polymorphic_on = "polymorphic_type", polymorphic_identity = "Object")

m_MedicalCondition = mapper_registry.map_imperatively(vet_clinic.MedicalCondition, t_MedicalCondition, polymorphic_on = "polymorphic_type", polymorphic_identity = "MedicalCondition")

m_affects = mapper_registry.map_imperatively(vet_clinic.affects, t_affects, properties = dict(left=relationship("MedicalCondition"), 
right=relationship("BiologicalObject")))

m_hasPart = mapper_registry.map_imperatively(vet_clinic.hasPart, t_hasPart, properties = dict(left=relationship("Object", foreign_keys=[t_hasPart.c.left_id]),
right=relationship("Object", foreign_keys=[t_hasPart.c.right_id])))

m_suffersFrom = mapper_registry.map_imperatively(vet_clinic.suffersFrom, t_suffersFrom, properties = dict(left=relationship("Animal"), 
right=relationship("MedicalCondition")))

m_BiologicalObject = mapper_registry.map_imperatively(vet_clinic.BiologicalObject, t_BiologicalObject, polymorphic_identity = "BiologicalObject", inherits = m_Object)

m_Injury = mapper_registry.map_imperatively(vet_clinic.Injury, t_Injury, polymorphic_identity = "Injury", inherits = m_MedicalCondition)

m_Animal = mapper_registry.map_imperatively(vet_clinic.Animal, t_Animal, polymorphic_identity = "Animal", inherits = m_BiologicalObject)

m_BodyPart = mapper_registry.map_imperatively(vet_clinic.BodyPart, t_BodyPart, polymorphic_identity = "BodyPart", inherits = m_BiologicalObject)

m_BrokenWing = mapper_registry.map_imperatively(vet_clinic.BrokenWing, t_BrokenWing, polymorphic_identity = "BrokenWing", inherits = m_Injury)

m_Bird = mapper_registry.map_imperatively(vet_clinic.Bird, t_Bird, polymorphic_identity = "Bird", inherits = m_Animal)

m_Mammal = mapper_registry.map_imperatively(vet_clinic.Mammal, t_Mammal, polymorphic_identity = "Mammal", inherits = m_Animal)

m_Reptile = mapper_registry.map_imperatively(vet_clinic.Reptile, t_Reptile, polymorphic_identity = "Reptile", inherits = m_Animal)

m_Wing = mapper_registry.map_imperatively(vet_clinic.Wing, t_Wing, polymorphic_identity = "Wing", inherits = m_BodyPart)

m_Canary = mapper_registry.map_imperatively(vet_clinic.Canary, t_Canary, polymorphic_identity = "Canary", inherits = m_Bird)

m_Cat = mapper_registry.map_imperatively(vet_clinic.Cat, t_Cat, polymorphic_identity = "Cat", inherits = m_Mammal)

m_Dog = mapper_registry.map_imperatively(vet_clinic.Dog, t_Dog, polymorphic_identity = "Dog", inherits = m_Mammal)
