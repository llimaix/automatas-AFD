from app.parser import parse_file

def test_bin01_even_ones():
    dfas = parse_file("data/automatas.txt")
    bin01 = dfas["BIN01"]
    assert bin01.simulate("")[0] is True          # 0 unos => par
    assert bin01.simulate("1")[0] is False        # 1 uno => impar
    assert bin01.simulate("11")[0] is True        # 2 unos => par
    assert bin01.simulate("10101")[0] is False    # 3 unos => impar
    assert bin01.simulate("101011")[0] is True    # 4 unos => par
