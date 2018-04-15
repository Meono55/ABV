import tempfile
import os
from shutil import copyfile
import pytest
from abv.most_recent_file import MostRecentFile


#Sets current working directory to ABV
def set_correct_cwd():
    while not os.getcwd().endswith('ABV'):
        os.chdir(os.path.dirname(os.getcwd()))

def test_chooses_most_recent_file():
    set_correct_cwd()
    temp_dir = tempfile.mkdtemp()
    # pylint: disable=unused-variable
    temp_file_past = tempfile.NamedTemporaryFile(dir=temp_dir, prefix='a')
    temp_file_most_recent = tempfile.NamedTemporaryFile(dir=temp_dir, prefix='b')
    source_file = os.path.abspath('tests/sample_csv_files/beer_data2018-04-14_16:34:24.131698.csv')
    copyfile(source_file, temp_file_most_recent.name)
    most_recent_file = MostRecentFile(temp_dir)
    test_iterator = iter(most_recent_file)
    beer_attributes = test_iterator.__next__()
    assert beer_attributes[0] == "ANGRY ORCHARD CRISP"
    assert beer_attributes[1] == "1/2 KEG"
    assert beer_attributes[2] == "CIDER"
    assert beer_attributes[3] == "0.00"
    assert beer_attributes[4] == "159.9500"
    assert beer_attributes[5] == "159.9500"
    assert beer_attributes[6] == "1"


def test_empty_file():
    set_correct_cwd()
    temp_dir = tempfile.mkdtemp()
    temp_file = tempfile.NamedTemporaryFile(dir=temp_dir)
    source_file = os.path.abspath('tests/sample_csv_files/empty.csv')
    copyfile(source_file, temp_file.name)
    most_recent_file = MostRecentFile(temp_dir)
    test_iterator = iter(most_recent_file)
    with pytest.raises(StopIteration):
        test_iterator.__next__()


def test_file_single_line():
    set_correct_cwd()
    temp_dir = tempfile.mkdtemp()
    temp_file = tempfile.NamedTemporaryFile(dir=temp_dir)
    source_file = os.path.abspath('tests/sample_csv_files/categories_only.csv')
    copyfile(source_file, temp_file.name)
    most_recent_file = MostRecentFile(temp_dir)
    test_iterator = iter(most_recent_file)
    with pytest.raises(StopIteration):
        test_iterator.__next__()

def test_empty_directory():
    set_correct_cwd()
    temp_dir = tempfile.mkdtemp()
    most_recent_file = MostRecentFile(temp_dir)
    test_iterator = iter(most_recent_file)
    with pytest.raises(StopIteration):
        test_iterator.__next__()


def test_full_single_file():
    count = 0
    set_correct_cwd()
    temp_dir = tempfile.mkdtemp()
    temp_file = tempfile.NamedTemporaryFile(dir=temp_dir)
    source_file = os.path.abspath('tests/sample_csv_files/beer_data2018-04-14_16:34:24.131698.csv')
    copyfile(source_file, temp_file.name)
    most_recent_file = MostRecentFile(temp_dir)
    test_iterator = iter(most_recent_file)
    for beer in test_iterator:
        if count == 0:
            assert beer[0] == "ANGRY ORCHARD CRISP"
            assert beer[1] == "1/2 KEG"
            assert beer[2] == "CIDER"
            assert beer[3] == "0.00"
            assert beer[4] == "159.9500"
            assert beer[5] == "159.9500"
            assert beer[6] == "1"
        if count == 8133 - 2:
            assert beer[0] == "THE COLONY MEADERY TEA TAX"
            assert beer[1] == "4/12 OZ CAN"
            assert beer[2] == "MEAD"
            assert beer[3] == "0.00"
            assert beer[4] == "23.8500"
            assert beer[5] == "123.4900"
            assert beer[6] == "6"
        count += 1
