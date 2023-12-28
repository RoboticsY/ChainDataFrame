import pandas as pd
import pytest

from ChainDF import ChainDF


class TestChainDF:
    def test_select(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [4, 5, 6],
            }
        )
        selected_df = ChainDF(df, deep_copy=True).select(["col1"]).value()
        assert selected_df.equals(pd.DataFrame({"col1": [1, 2, 3]}))

        # 引数の型チェック
        with pytest.raises(TypeError):
            ChainDF(df, deep_copy=True).select("col1")

        # 存在しないカラムを指定した場合
        not_exist_col = "not_exist_col"
        with pytest.raises(KeyError):
            ChainDF(df, deep_copy=True).select([not_exist_col])

        # 返り値の型チェック
        df_types = ChainDF(df, deep_copy=True).select(["col1"])
        assert isinstance(df_types, ChainDF)

    def test_fileter(self):
        int_df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [4, 5, 6],
            }
        )
        filtered_int_df = ChainDF(int_df, deep_copy=True).filter("col1", 1).value()
        assert filtered_int_df.equals(pd.DataFrame({"col1": [1], "col2": [4]}))

        str_df = pd.DataFrame(
            {
                "col1": ["a", "b", "c"],
                "col2": ["d", "e", "f"],
            }
        )
        filtered_str_df = ChainDF(str_df, deep_copy=True).filter("col1", "a").value()
        assert filtered_str_df.equals(pd.DataFrame({"col1": ["a"], "col2": ["d"]}))

        with pytest.raises(TypeError):
            ChainDF(int_df, deep_copy=True).filter(["col1"], "a")

        with pytest.raises(TypeError):
            ChainDF(int_df, deep_copy=True).filter("col1", ["a"])

    def test_value(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [4, 5, 6],
            }
        )
        chain_df = ChainDF(df, deep_copy=True).value()
        assert isinstance(chain_df, pd.DataFrame)
        assert chain_df.equals(df)

    def test_sum(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [0.1, -4, 10010],
            }
        )
        col1_sum = ChainDF(df, deep_copy=True).sum("col1")
        assert col1_sum == 6

        col2_sum = ChainDF(df, deep_copy=True).sum("col2")
        assert col2_sum == (0.1 - 4 + 10010)

        with pytest.raises(TypeError):
            ChainDF(df, deep_copy=True).sum(1)

        with pytest.raises(KeyError):
            ChainDF(df, deep_copy=True).sum("not_exist_col")

    def test_mean(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [0.1, -4, 10010],
            }
        )
        col1_mean = ChainDF(df, deep_copy=True).mean("col1")
        assert col1_mean == (1 + 2 + 3) / 3.0

        col2_mean = ChainDF(df, deep_copy=True).mean("col2")
        assert col2_mean == (0.1 - 4 + 10010) / 3.0

        with pytest.raises(TypeError):
            ChainDF(df, deep_copy=True).mean(1)

        with pytest.raises(KeyError):
            ChainDF(df, deep_copy=True).mean("not_exist_col")

    def test_median(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [0.1, -4, 10010],
            }
        )
        col1_median = ChainDF(df, deep_copy=True).median("col1")
        assert col1_median == 2

        col2_median = ChainDF(df, deep_copy=True).median("col2")
        assert col2_median == 0.1

        with pytest.raises(TypeError):
            ChainDF(df, deep_copy=True).median(1)

        with pytest.raises(KeyError):
            ChainDF(df, deep_copy=True).median("not_exist_col")

        df_even = pd.DataFrame(
            {
                "col1": [1, 2, 3, 4],
                "col2": [0.1, -4, 10010, 100],
            }
        )
        col1_median = ChainDF(df_even, deep_copy=True).median("col1")
        assert col1_median == (2 + 3) / 2.0

    def test_max(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [0.1, -4, 10010],
            }
        )
        col1_max = ChainDF(df, deep_copy=True).max("col1")
        assert col1_max == 3

        col2_max = ChainDF(df, deep_copy=True).max("col2")
        assert col2_max == 10010

        with pytest.raises(TypeError):
            ChainDF(df, deep_copy=True).max(1)

        with pytest.raises(KeyError):
            ChainDF(df, deep_copy=True).max("not_exist_col")

    def test_min(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [0.1, -4, 10010],
            }
        )
        col1_min = ChainDF(df, deep_copy=True).min("col1")
        assert col1_min == 1

        col2_min = ChainDF(df, deep_copy=True).min("col2")
        assert col2_min == -4

        with pytest.raises(TypeError):
            ChainDF(df, deep_copy=True).min(1)

        with pytest.raises(KeyError):
            ChainDF(df, deep_copy=True).min("not_exist_col")

    def test_count(self):
        df = pd.DataFrame(
            {
                "col1": ["aaa", "bbb", "aaa"],
                "col2": [0.1, -4, 10010],
            }
        )
        col1_count = ChainDF(df, deep_copy=True).count("col1", "aaa")
        print(col1_count)
        assert col1_count == 2

        col1_count_zero = ChainDF(df, deep_copy=True).count("col1", "ccc")
        assert col1_count_zero == 0

        col2_count = ChainDF(df, deep_copy=True).count("col2", -4)
        assert col2_count == 1

        col2_count_float = ChainDF(df, deep_copy=True).count("col2", 0.1)
        assert col2_count_float == 1

        with pytest.raises(TypeError):
            ChainDF(df, deep_copy=True).count(1, 10)

        with pytest.raises(KeyError):
            ChainDF(df, deep_copy=True).count("not_exist_col", 10)
