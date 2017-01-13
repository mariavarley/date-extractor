#-*- coding: utf-8 -*-

from sys import version_info
python_version = version_info.major

import unittest
from date_extractor import *

class TestStringMethods(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(str(g("12/23/09")), "2009-12-23 00:00:00+00:00")

    def test_year(self):
        self.assertEqual(str(g("2015-11-21")),'2015-01-01 00:00:00+00:00')

    def test_arabic(self):
        if python_version == 2:
            text = "٢١ نوفمبر ٢٠١٥".decode('utf-8')
            try:
                self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')
            except Exception as e:
                print "FAILED ON text:", [text]
                raise e
        elif python_version == 3:
            text = "٢١ نوفمبر ٢٠١٥"
            self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')



    def test_arabic2(self):
        text = """
        ٢١ تشرين ثاني/نوفمبر ٢٠١٥
        """
        if python_version == 2:
            text = text.decode("utf-8")
        self.assertEqual(str(g(text)),'2015-11-21 00:00:00+00:00')

    def test_year(self):
        text = """12/16/2010 9:09 AM ET\nA Run Like No Othe"""
        self.assertEqual(str(g(text)), '2010-12-16 00:00:00+00:00')

    def test_year_by_itself(self):
        text = "President Obama has used Oval Office speeches sparingly, compared with previous presidents. His previous two addresses, both in 2010, covered the Deepwater Horizon oil spill and the end of combat operations in Iraq."
        self.assertEqual(str(g(text)), '2010-01-01 00:00:00+00:00')

    def test_mdyt(self):
        text = "9/1/99 22:00"
        self.assertEqual(str(g(text)), "1999-09-01 00:00:00+00:00")


    def test_future_dates(self):
        source_expected = [
            ('can you find correct date here 2033', '2033-01-01 00:00:00+00:00'),
            ('can you find correct date here june 2033', '2033-06-01 00:00:00+00:00'),
            ('can you find correct date here 2 june 2033', '2033-06-02 00:00:00+00:00'),
            ('can you find correct date here 12 january 2018', '2018-01-12 00:00:00+00:00'),
            ('can you find correct date here 1 january 2018', '2018-01-01 00:00:00+00:00'),
            ('can you find correct date here 31 april 2017', 'None'),
            ('can you find correct date here 32 december 2017', 'None')
        ]

        for source, expected in source_expected:
            #print "sourece:", source
            extracted_as_list = (extract_dates(source) or [None])[0]
            #print "extracted_as_list:", extracted_as_list
            self.assertEqual(str(extracted_as_list), expected)

            extracted_as_single = extract_date(source)
            #print "extracted_as_single:", extracted_as_single
            self.assertEqual(str(extracted_as_single), expected)


if __name__ == '__main__':
    unittest.main()
