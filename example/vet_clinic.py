from dataclasses import dataclass

@dataclass
class MedicalCondition:
    ...


@dataclass
class Object:
    hasMass: float


@dataclass
class Injury(MedicalCondition):
    ...


@dataclass
class BiologicalObject(Object):
    ...


@dataclass
class BrokenWing(Injury):
    ...


@dataclass
class Animal(BiologicalObject):
    ...


@dataclass
class BodyPart(BiologicalObject):
    ...


@dataclass
class Bird(Animal):
    ...


@dataclass
class Mammal(Animal):
    ...


@dataclass
class Reptile(Animal):
    ...


@dataclass
class Wing(BodyPart):
    ...


@dataclass
class Canary(Bird):
    ...


@dataclass
class Cat(Mammal):
    ...


@dataclass
class Dog(Mammal):
    ...


@dataclass
class affects:
    left: MedicalCondition
    right: BiologicalObject

@dataclass
class hasPart:
    left: Object
    right: Object

@dataclass
class suffersFrom:
    left: Animal
    right: MedicalCondition

