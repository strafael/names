import names

def test_names():
    n = names.Names()
    assert len(n.gen()) > 0


def test_gen_with_start():
    start = "rafa"
    n = names.Names()
    result = n.gen_with_start(start)
    assert result.startswith(start)
