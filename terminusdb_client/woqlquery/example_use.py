from typing import List, Optional, Set

from terminusdb_client.woqlquery.woql_schema import (
    DocumentTemplate,
    EnumTemplate,
    ObjectTemplate,
    WOQLSchema,
)

# from woql_schema import WOQLSchema, Document, Property, WOQLObject

my_schema = WOQLSchema()


class MyObject(ObjectTemplate):
    _schema = my_schema


class MyDocument(DocumentTemplate):
    _schema = my_schema


class Coordinate(MyObject):
    x: float
    y: float


class Country(MyDocument):
    name: str
    perimeter: List[Coordinate]


class Address(MyObject):
    street: str
    country: Country


class Person(MyDocument):
    name: str
    age: int
    friend_of: Set["Person"]


class Employee(Person):
    address_of: Address
    contact_number: Optional[str]
    managed_by: "Employee"


class Team(EnumTemplate):
    _schema = my_schema
    IT = ()
    Marketing = ()


# print(dir(Person))
# print(Person.to_dict())

# print(my_schema.all_obj())
# print(Team.__members__)
print(my_schema.to_dict())
