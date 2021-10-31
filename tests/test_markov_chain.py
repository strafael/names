import pathlib
import pkg_resources
import pytest

from names.markov import MarkovChain
from names.reader import pipeline

DATA_PATH = pathlib.Path(pkg_resources.resource_filename("names", "data"))


@pytest.fixture
def model():
    filename = DATA_PATH.joinpath("firstnames/samples/conhecidos.txt")
    source = pipeline(filename)
    m = MarkovChain()
    m.build(source)
    yield m


def test_markov_chain():
    m = MarkovChain()
    m.build(["foo"])
    assert len(m.gen()) > 0


def test_gen_with_start(model):
    start = "r"
    result = model.gen_with_start(start)
    assert result.startswith(start)


def test_gen_with_start_4_chars(model):
    start = "rafa"
    with pytest.raises(ValueError):
        result = model.gen_with_start(start)
