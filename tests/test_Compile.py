

import pytest
import unittest

import os
from pathlib import Path

from parametric_plasma_source.plasma import Plasma

pytest.importorskip("openmc")

class test_object_properties(unittest.TestCase):

        def test_compile(self):

                os.system('test_plasma.so')
                test_plasma = Plasma()
                test_plasma.export_plasma_source('test_plasma.so')

                assert Path('test_plasma.so').exists() == True
                os.system('rm test_plasma.so')


if __name__ == '__main__':
        unittest.main()
