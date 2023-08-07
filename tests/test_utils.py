from unittest import TestCase

from api.utils import * 

class UtilsTest(TestCase):
    def test_get_dates_from_parameters_search_date(self):
        query_params = {'search_date': '2023-03-01'}
        expected = ['2023-03-01']
        actual = get_dates_from_parameters(query_params)
        assert expected == actual

    def test_get_dates_from_parameters_start_end_date(self):
        query_params = {'start_date': '2023-03-01', 'end_date': '2023-03-02'}
        expected = ['2023-03-01', '2023-03-02']
        actual = get_dates_from_parameters(query_params)
        assert expected == actual 

        query_params = {'start_date': '2023-03-01', 'end_date': '2023-04-1'}
        expected = [f'2023-03-{str(a).zfill(2)}' for a in range(1,32)]
        expected.append('2023-04-01')
        actual = get_dates_from_parameters(query_params)
        assert expected == actual
    
    def test_ignore_empty_search_date(self):
        query_params = {
            'search_date': None,
            'start_date': '2023-01-01',
            'end_date': '2023-01-03'
        }
        expected = ['2023-01-01', '2023-01-02', '2023-01-03']
        actual = get_dates_from_parameters(query_params)
        assert expected == actual
