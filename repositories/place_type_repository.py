from __future__ import annotations
from repositories.gramps_type_repository import GrampsTypeRepository

class PlaceTypeRepository(GrampsTypeRepository):
    BOROUGH = 13
    BUILDING = 19
    CITY = 4
    COUNTRY = 1
    COUNTY = 3
    CUSTOM = 0
    DEPARTMENT = 10
    DISTRICT = 12
    FARM = 18
    HAMLET = 17
    LOCALITY = 6
    MUNICIPALITY = 14
    NEIGHBORHOOD = 11
    NUMBER = 20
    PARISH = 5
    PROVINCE = 8
    REGION = 9
    STATE = 2
    STREET = 7
    TOWN = 15
    UNKNOWN = -1
    VILLAGE = 16

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
