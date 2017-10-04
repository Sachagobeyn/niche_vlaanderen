from unittest import TestCase

import numpy as np
import rasterio

import niche_vlaanderen


def raster_to_numpy(filename):
    '''Read a GDAL grid as numpy array

    Notes
    ------
    No-data values are -99 for integer types and np.nan for real types.
    '''
    with rasterio.open(filename) as ds:
        data = ds.read(1)
        nodata = ds.nodatavals[0]

    # create a mask for no-data values, taking into account the data-types
    if data.dtype == 'float32':
        data[data == nodata] = np.nan
    else:
        data[data == nodata] = -99

    return data


class testNutrientLevel(TestCase):

    def test_nitrogen_mineralisation(self):
        soil_codes = np.array([140000])
        msw = np.array([33])
        nl = niche_vlaanderen.NutrientLevel()
        result = nl._get_mineralisation(soil_codes, msw)
        np.testing.assert_equal(np.array([75]), result)

    def test_borders(self):
        soil_codes = np.array([10000, 10000, 10000, 10000, 10000])
        msw = np.array([4, 5, 7, 10, 11])
        nl = niche_vlaanderen.NutrientLevel()
        result_nm = nl._get_mineralisation(soil_codes, msw)
        expected_nm = np.array([50, 50, 55, 55, 76])
        np.testing.assert_equal(expected_nm, result_nm)
        nuls = np.array([0, 0, 0, 0, 0])
        # we want to check the boundaries ]156, 293]
        nitrogen_sum = np.array([155, 156, 200, 293,294])
        # so we substract the nitrogen_sum from the expected mineralisation
        nitrogen_animal = nitrogen_sum - expected_nm
        management = np.array([2, 2, 2, 2, 2])
        result = nl.calculate(soil_code=soil_codes,
                     msw=msw,
                     management=management,
                     nitrogen_animal=nitrogen_animal,
                     nitrogen_atmospheric=nuls,
                     nitrogen_fertilizer=nuls,
                     inundation=nuls)
        expected = np.array([2, 2, 3, 3, 4])
        np.testing.assert_equal(expected, result)

    def test__get(self):

        management = np.array([2])
        soil_code = np.array([140000])
        nitrogen = np.array([445])
        inundation = np.array([1])

        nl = niche_vlaanderen.NutrientLevel()
        result = nl._get(management, soil_code, nitrogen, inundation)
        np.testing.assert_equal(np.array(5), result)

    def test_calculate(self):
        nl = niche_vlaanderen.NutrientLevel()
        management = np.array([2])
        soil_code = np.array([140000])
        msw = np.array([33])
        nitrogen_deposition = np.array([20])
        nitrogen_animal = np.array([350])
        nitrogen_fertilizer = np.array([0])
        inundation = np.array([1])
        result = nl.calculate(soil_code, msw, nitrogen_deposition,
                              nitrogen_animal, nitrogen_fertilizer, management,
                              inundation)

        np.testing.assert_equal(np.array([5]), result)

    def test_nutrient_level_testcase(self):
        nl = niche_vlaanderen.NutrientLevel()
        soil_code = raster_to_numpy("testcase/input/soil_codes.asc")
        msw = raster_to_numpy("testcase/input/msw.asc")
        nitrogen_deposition = \
            raster_to_numpy("testcase/input/nitrogen_atmospheric.asc")
        nitrogen_animal = raster_to_numpy("testcase/input/nitrogen_animal.asc")
        nitrogen_fertilizer = raster_to_numpy("testcase/input/nullgrid.asc")
        inundation = \
            raster_to_numpy("testcase/input/inundation_nutrient_level.asc")
        management = raster_to_numpy("testcase/input/management.asc")

        nutrient_level = \
            raster_to_numpy("testcase/intermediate/nutrient_level.asc")
        result = nl.calculate(soil_code, msw, nitrogen_deposition,
                              nitrogen_animal, nitrogen_fertilizer, management,
                              inundation)

        np.testing.assert_equal(nutrient_level, result)
