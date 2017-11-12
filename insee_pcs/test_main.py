import unittest

from main import PCS, get_PCS, get_all_PCS_of_level, _check_level

class TestPCSDB(unittest.TestCase):
    def test_numbers(self):
        # Grand total.
        self.assertEqual(len(PCS.select()), 571)
        # Level 1.
        self.assertEqual(len(get_all_PCS_of_level(1)), 8)
        # Level 2.
        self.assertEqual(len(get_all_PCS_of_level(2)), 24)
        # Level 3.
        self.assertEqual(len(get_all_PCS_of_level(3)), 42)
        # Level 4.
        self.assertEqual(len(get_all_PCS_of_level(4)), 497)
    
    def test_INSEE_url(self):
        self.assertEqual(
            get_PCS(1, '1').INSEE_url(),
            "https://insee.fr/fr/metadonnees/pcs2003/categorieSocioprofessionnelleAgregee/1"
        )
        self.assertEqual(
            get_PCS(2, '10').INSEE_url(),
            "https://insee.fr/fr/metadonnees/pcs2003/categorieSocioprofessionnelle/10"
        )
        self.assertEqual(
            get_PCS(3, '22').INSEE_url(),
            "https://insee.fr/fr/metadonnees/pcs2003/categorieSocioprofessionnelleDetaillee/22"
        )
        self.assertEqual(
            get_PCS(4, '227d').INSEE_url(),
            "https://insee.fr/fr/metadonnees/pcs2003/professionRegroupee/227d"
        )
    
    def test_iter_children(self):
        start_pcs = get_PCS(1, '1')
        children = list(start_pcs.iter_children())
        expected_codes = [
            '1', '10', '11', '111a', '111b', '111c', '111d', '111e',
            '111f', '12', '121a', '121b', '121c', '121d', '121e',
            '121f', '122a', '122b', '122c', '13', '131a', '131b',
            '131c', '131d', '131e', '131f'
        ]
        self.assertEqual([p.code for p in children], expected_codes)
        
        start_pcs = get_PCS(1, '3')
        children = list(start_pcs.iter_children())
        expected_codes = [
            '3', '31', '31', '311a', '311b', '311c', '311d', '311e',
            '311f', '312a', '312b', '312c', '312d', '312e', '312f',
            '312g', '313a', '32', '33', '331a', '332a', '332b',
            '333a', '333b', '333c', '333d', '333e', '333f', '334a',
            '335a', '34', '341a', '341b', '342a', '342e', '343a',
            '344a', '344b', '344c', '344d', '35', '351a', '352a',
            '352b', '353a', '353b', '353c', '354a', '354b', '354c',
            '354d', '354g', '36', '37', '371a', '372a', '372b', '372c',
            '372d', '372e', '372f', '373a', '373b', '373c', '373d',
            '374a', '374b', '374c', '374d', '375a', '375b', '376a',
            '376b', '376c', '376d', '376e', '376f', '376g', '377a',
            '38', '380a', '381a', '382a', '382b', '382c', '382d',
            '383a', '383b', '383c', '384a', '384b', '384c', '385a',
            '385b', '385c', '386a', '386d', '386e', '387a', '387b',
            '387c', '387d', '387e', '387f', '388a', '388b', '388c',
            '388d', '388e', '389a', '389b', '389c'
        ]
        self.assertEqual([p.code for p in children], expected_codes)
        
        start_pcs = get_PCS(1, '3')
        children = list(start_pcs.iter_children(max_level=3))
        expected_codes = [
            '3', '31', '31', '32', '33', '34', '35', '36', '37', '38'
        ]
        self.assertEqual([p.code for p in children], expected_codes)
        
        start_pcs = get_PCS(1, '1')
        children = list(start_pcs.iter_children(max_level=1))
        self.assertEqual([p.code for p in children], ['1'])
    
    def test_all_parents(self):
        start_pcs = get_PCS(1, '3')
        parents = start_pcs.all_parents()
        self.assertEqual(['3'], [p.code for p in parents])
        
        start_pcs = get_PCS(4, '382b')
        parents = start_pcs.all_parents()
        expected_codes = ['382b', '38', '36', '3']
        self.assertEqual(expected_codes, [p.code for p in parents])
        
        start_pcs = get_PCS(4, '382b')
        parents = start_pcs.all_parents(include_self=False)
        expected_codes = ['38', '36', '3']
        self.assertEqual(expected_codes, [p.code for p in parents])

class TestUtils(unittest.TestCase):
    def test_getter(self):
        self.assertEqual(get_PCS(1, '1').code, '1')
        self.assertEqual(get_PCS(1, '2').code, '2')
        
        self.assertEqual(get_PCS(2, '10').code, '10')
        
        self.assertEqual(get_PCS(3, '22').code, '22')
        self.assertEqual(get_PCS(4, '227d').code, '227d')
        self.assertEqual(get_PCS(4, '8600').code, '8600')
        
        with self.assertRaises(ValueError):
            get_PCS(1, '10')
        with self.assertRaises(ValueError):
            get_PCS(2, '19')
        with self.assertRaises(ValueError):
            get_PCS(3, '124')
        with self.assertRaises(ValueError):
            get_PCS(4, '999b')
    
    def test_check_level(self):
        # Must be ok.
        for i in range(1, 5):
            _check_level(i)
        with self.assertRaises(ValueError):
            _check_level(5)
        with self.assertRaises(ValueError):
            _check_level('5')
        with self.assertRaises(ValueError):
            _check_level(0)

if __name__ == "__main__":
    unittest.main()
