import pytest

def test_addition():
    assert 1 + 1 == 2

def test_strings():
    assert "hello" + "world" == "helloworld"

def test_list_length():
    assert len([1, 2, 3]) == 3

def test_dictionary():
    d = {"a": 1, "b": 2}
    assert "a" in d

def test_boolean():
    assert True is True