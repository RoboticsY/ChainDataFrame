# pandas の ユーティリティ関数を管理
from __future__ import annotations

import copy
from typing import Callable

import pandas as pd


class ChainDF:
    """pandas のデータフレームをメソッドチェーンできるようにするクラス"""

    def __init__(self, df: pd.DataFrame, deep_copy: bool = False):
        """コンストラクタ

        Args:
            df (pd.DataFrame): pandas.DataFrame インスタンス

            deep_copy (bool, optional): df をディープコピーするフラグ。デフォルトは False で、ディープコピーしない。

        Raises:
            TypeError: df が pandas.DataFrame 型でない場合に発生

        Examples:
            >>> import pandas as pd
            >>> from ChainDF import ChainDF
            >>> df = pd.DataFrame({
            ...     'col1': [1, 2, 3],
            ...     'col2': [4, 5, 6],
            ... })
            >>> chain_df = ChainDF(df, deep_copy=True)
            >>> chain_df.select(['col1']).value()
                col1
            0     1
            1     2
            2     3

        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be pandas.DataFrame")
        if deep_copy:
            self.df: pd.DataFrame = copy.deepcopy(df)
        else:
            self.df: pd.DataFrame = df

    def filter(self, column_name: str, condition: str | int | float) -> ChainDF:
        """DataFrame から条件に合う行のみを抽出する。

        指定されたカラムの値が、指定された値と一致する行のみを残す。

        Args:
            column_name (str): カラム名

            condition (str | int | float): 指定されたカラムの値と完全一致する値

        Raises:
            TypeError: column_name が str 型でない場合に発生

            TypeError: condition が str または int または float 型でない場合に発生

        Returns:
            ChainDF: 指定されたカラムの値が、指定された値と一致する行のみを残した当該インスタンス

        Notes:
            将来的に完全一致以外の条件に対応するため、引数の構成に破壊的な変更を加える可能性があります。

        """
        if not isinstance(column_name, str):
            raise TypeError("column_name must be str")
        if not isinstance(condition, (str, int, float)):
            raise TypeError("condition must be str or int or float")
        self.df = self.df[self.df[column_name] == condition]
        return self

    def select(self, column_names: list) -> ChainDF:
        """DataFrame から指定した列のみを抽出する。

        引数で指定されたカラム名と一致する列のみを残した DataFrame を生成します。

        Args:
            column_names (list): カラム名のリスト

        Raises:
            TypeError: column_names が list 型でない場合に発生

        Returns:
            ChainDF: 指定されたカラムのみを残した当該インスタンス

        """
        if not isinstance(column_names, list):
            raise TypeError("column_names must be list")
        self.df = self.df[column_names]
        return self

    # データフレームを連結する
    def concat(self, df: pd.DataFrame) -> ChainDF:
        # axis=1 で横方向に連結する
        self.df = pd.concat([self.df, df], axis=1)
        return self

    # 特定のカラムを加工する
    def calc_col(self, column_name: str, func: Callable) -> ChainDF:
        self.df[column_name] = self.df[column_name].apply(func)
        return self

    # 特定のカラムを加工して、新規にカラムを追加する
    def calc_and_add_col(self, from_col: str, new_col: str, func: Callable) -> ChainDF:
        self.df[new_col] = self.df[from_col].apply(func)
        return self

    # 複数のカラムを加工して、新規にカラムを追加する
    def calc_and_add_col_from_multi_cols(
        self, from_cols: list, new_col: str, func: Callable
    ) -> ChainDF:
        self.df[new_col] = self.df[from_cols].apply(func, axis=1)
        return self

    def value(self) -> pd.DataFrame:
        """インスタンス内部の pandas.DataFrame を取得する

        Returns:
            pd.DataFrame: インスタンス内部の pandas.DataFrame

        """
        return self.df

    def sum(self, column_name: str) -> int | float:
        """任意のカラムの合計値を取得する

        Args:
            column_name (str): カラム名

        Raises:
            TypeError: column_name が str 型でない場合に発生

            KeyError: カラム名が存在しない場合に発生

        Returns:
            int | float: 指定されたカラムの合計値

        """
        self.__columun_name_validation(column_name)
        return self.df[column_name].sum()

    def mean(self, column_name: str) -> int | float:
        """任意のカラムの平均値を取得する

        Args:
            column_name (str): カラム名

        Raises:
            TypeError: column_name が str 型でない場合に発生

            KeyError: カラム名が存在しない場合に発生

        Returns:
            int | float: 指定されたカラムの平均値

        """
        self.__columun_name_validation(column_name)
        return self.df[column_name].mean()

    def median(self, column_name: str) -> int | float:
        """任意のカラムの中央値を取得する

        Args:
            column_name (str): カラム名

        Raises:
            TypeError: column_name が str 型でない場合に発生

            KeyError: カラム名が存在しない場合に発生

        Returns:
            int | float: 指定されたカラムの中央値

        """
        self.__columun_name_validation(column_name)
        return self.df[column_name].median()

    def max(self, column_name: str) -> int | float:
        """指定されたカラムの最大値を取得する

        Args:
            column_name (str): カラム名

        Raises:
            TypeError: column_name が str 型でない場合に発生

            KeyError: カラム名が存在しない場合に発生

        Returns:
            int | float: 指定されたカラムの最大値

        """
        self.__columun_name_validation(column_name)
        return self.df[column_name].max()

    def min(self, column_name: str) -> int | float:
        """指定されたカラムの最小値を取得する

        Args:
            column_name (str): カラム名

        Raises:
            TypeError: column_name が str 型でない場合に発生

            KeyError: カラム名が存在しない場合に発生

        Returns:
            int | float: 指定されたカラムの最小値

        """
        self.__columun_name_validation(column_name)
        return self.df[column_name].min()

    def get75perTile(self, column_name: str) -> int | float:
        """指定されたカラムの 75% タイル値を取得する"""
        self.__columun_name_validation(column_name)
        return self.df[column_name].quantile(0.75)

    def count(self, column_name: str, condition: str | int | float) -> int:
        """指定されたカラムの特定の値の出現回数をカウントする

        Args:
            column_name (str): カラム名

            condition (str | int | float): カウント対象の値

        Raises:
            TypeError: column_name が str 型でない場合に発生

            TypeError: condition が str, int, float 型でない場合に発生

            KeyError: カラム名が存在しない場合に発生

        Returns:
            int: 指定されたカラムの特定の値の出現回数

        """
        self.__columun_name_validation(column_name)
        if not isinstance(condition, (str, int, float)):
            raise TypeError("condition must be str or int or float")
        return self.filter(column_name, condition).value().shape[0]

    def get_column_names(self) -> list:
        """インスタンス内部の pandas.DataFrame のカラム名のリストを取得する

        Returns:
            list: インスタンス内部の pandas.DataFrame のカラム名のリスト

        """
        return self.df.columns.tolist()

    def __columun_name_validation(self, column_name: str) -> None:
        """カラム名の型チェック & 存在チェックを行う

        Args:
            column_name (str): カラム名

        Raises:
            TypeError: column_name が str 型でない場合に発生

            KeyError: カラム名が存在しない場合に発生

        """
        if not isinstance(column_name, str):
            raise TypeError("column_name must be str")
        if column_name not in self.get_column_names():
            raise KeyError(f"column_name {column_name} is not in DataFrame")
