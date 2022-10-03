from subprocess import call


class TestTetrisFunction:
    """
    This test checks if passes in the contents of tests/test_input.txt to the tetris engine
    and confirms if the remaining number of tetris lines are 2, 1, 4 and 3 for each line of input
    respectively.
    """
    def test_file_output(self, tmpdir):
        output_location = tmpdir.join("test_output.txt")
        
        call(["python3", "tetris_engine.py", "tests/test_input.txt", str(output_location)])
        
        
        assert output_location.read() == "2\n1\n4\n3\n"
        assert len(tmpdir.listdir()) == 1
 
        