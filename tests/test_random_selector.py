import pathlib
import pkg_resources
import pytest

from names.random import RandomSelector
from names.reader import pipeline

DATA_PATH = pathlib.Path(pkg_resources.resource_filename("names", "data"))


@pytest.fixture
def model():
    filename = DATA_PATH.joinpath("firstnames/samples/animais.txt")
    source = pipeline(filename)
    m = RandomSelector()
    m.build(source)
    yield m


def test_random_selector():
    m = RandomSelector()
    m.build(["foo"])
    assert len(m.gen()) > 0


def test_gen_with_start(model):
    start = "t"
    result = model.gen_with_start(start)
    assert result.startswith(start)
