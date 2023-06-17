import pytest
from ChainDF import ChainDF
import pandas as pd


class TestConstructor:

    def test_constructor(self):
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6],
        })
        assert ChainDF(df).value() is df
        assert ChainDF(df).value().equals(df)

    def test_constructor_deep_copy(self):
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6],
        })
        assert ChainDF(df, deep_copy=True).value() is not df
        assert ChainDF(df, deep_copy=True).value().equals(df)

    @pytest.mark.parametrize('arg', [
        None,
        1,
        1.0,
        'str',
        [],
        (),
        {},
    ])
    def test_constructor_raise_TypeError(self, arg):
        with pytest.raises(TypeError):
            ChainDF(arg)

        with pytest.raises(TypeError):
            ChainDF(arg, deep_copy=True)
