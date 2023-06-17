
# pandas の ユーティリティ関数を管理
from __future__ import annotations
import copy
import pandas as pd

class ChainDF:
    '''pandas のデータフレームをメソッドチェーンできるようにするクラス'''

    def __init__(self, df: pd.DataFrame, deep_copy: bool = False):
        ''' コンストラクタ

        Args
        ----------
        df : pd.DataFrame
            データフレーム
        deep_copy : bool, optional
            データフレームをディープコピーするフラグ
            デフォルトは False で、ディープコピーしない。
        ----------
        '''
        if not isinstance(df, pd.DataFrame):
            raise TypeError('df must be pandas.DataFrame')
        if deep_copy:
            self.df: pd.DataFrame = copy.deepcopy(df)
        else:
            self.df: pd.DataFrame = df
    
    # 指定されたカラムのうち、条件を満たす行のみを残す。
    def filter(self, column_name: str, condition: str | int | float) -> ChainDF:
        self.df = self.df[self.df[column_name] == condition]
        return self

    # pandas のデータフレーム内で指定されたカラムの列だけ残したデータフレームを返す。
    def select(self, column_names: list) -> ChainDF:
        self.df = self.df[column_names]
        return self
    
    # データフレームを連結する
    def concat(self, df: pd.DataFrame) -> ChainDF:
        # axis=1 で横方向に連結する
        self.df = pd.concat([self.df, df], axis=1)
        return self
    
    # 特定のカラムを加工する
    def calc_col(self, column_name: str, func: function) -> ChainDF:
        self.df[column_name] = self.df[column_name].apply(func)
        return self
    
    # 特定のカラムを加工して、新規にカラムを追加する
    def calc_and_add_col(self, from_col: str, new_col: str, func: function) -> ChainDF:
        self.df[new_col] = self.df[from_col].apply(func)
        return self
    
    # 複数のカラムを加工して、新規にカラムを追加する
    def calc_and_add_col_from_multi_cols(self, from_cols: list, new_col: str, func: function) -> ChainDF:
        self.df[new_col] = self.df[from_cols].apply(func, axis=1)
        return self

    # データフレームを取得する
    def value(self) -> pd.DataFrame:
        return self.df
    
    # 任意のカラムの合計値を取得する
    def sum(self, column_name: str) -> int | float:
        return self.df[column_name].sum()
    
    # 任意のカラムの平均値を取得する
    def mean(self, column_name: str) -> int | float:
        return self.df[column_name].mean()
    
    # 任意のカラムの中央値を取得する
    def median(self, column_name: str) -> int | float:
        return self.df[column_name].median()
    
    # 任意のカラムの最大値を取得する
    def max(self, column_name: str) -> int | float:
        return self.df[column_name].max()
    
    # 任意のカラムの最小値を取得する
    def min(self, column_name: str) -> int | float:
        return self.df[column_name].min()
    
    # 任意のカラムの特定の値の出現回数をカウントする
    def count(self, column_name: str, condition: str | int | float) -> int:
        return self.filter(column_name, condition).value().shape[0]
