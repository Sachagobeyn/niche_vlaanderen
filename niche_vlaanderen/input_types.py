from enum import Enum

class InputLayerTypes(Enum):
    BORDER = 1
    REGION = 2
    SOIL_CODE = 3
    MLW = 4
    MSW = 5
    MHW = 6
    SEEPAGE = 7
    NUTRIENT_LEVEL = 8
    INUNDATION_ACIDITY = 9
    NITROGEN_ATMOSPHERIC = 10
    NITROGEN_ANIMAL = 11
    NITROGEN_FERTILIZER = 12
    MANAGEMENT = 13
    CONDUCTIVITY = 14
    REGENLENS = 15
    INUNDATION_VEGETATION = 16
    NULLGRID = 17
