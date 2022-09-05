import pytest

from tetris_file import tetris_runner


class TestTetrisFunction:
    """
    Test the tetris builder function on the provided examples.
    """
    def test_tetris_function(self):
        assert tetris_runner('Q0') == '2',  "Result should be 2"
        
    def test_tetris_function(self):
        assert tetris_runner('I0,I4,Q8') == '1',  "Result should be 1"
        
    def test_tetris_function(self):
        assert tetris_runner('T1,Z3,I4') == '4',  "Result should be 4"
        
    def test_tetris_function(self):
        assert tetris_runner('Q0,I2,I6,I0,I6,I6,Q2,Q4') == '3',  "Result should be 3"