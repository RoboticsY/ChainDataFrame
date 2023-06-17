# ChainDataFrame
ChainDataFrame は、pandas DataFrame 操作の可読性を向上させるためのラッパーライブラリです。

日本語を母国語とする人のうち、DataFrame のメンテナンス性が悪く、苦痛を感じている方をターゲットにしているため、ドキュメント類も極力日本語を使用します。

## 使い方

### インストール
このリポジトリから直接インストールしてください。

```bash
pip install git+https://github.com/RoboticsY/ChainDataFrame.git
```

### アップデート
```bash
pip install -U git+https://github.com/RoboticsY/ChainDataFrame.git
```

### インポート

```python
from ChainDF import ChainDF
```

### サンプルコード

(例) 特定の列や業を抽出
```python
import pandas as pd
from ChainDF import ChainDF

df = pd.read_csv('xxxx.csv')
# 'ColA' と 'ColB' の列のうち、colA が 'xxx' かつ colB が 'yyy' の行を抽出する
# () で囲むとメソッドチェーンが見やすいのでおすすめです。
new_df = (ChainDF(df)
            .select(['colA', 'colB']) # 列の抽出
            .filter('colA', 'xxx') # 条件に合致する行の抽出
            .filter('colB', 'yyy') # 条件に合致する行の抽出
            .value() # pandas DataFrame をリターン
            )
```

(例) 複数列を参照して新しい列を作成
```python
import pandas as pd
from ChainDF import ChainDF

def add(cols):
    return cols[0] + cols[1]

df = pd.DataFrame({
    'colA': [1, 2, 3, 3],
    'colB': [4, 5, 6, 6],
    'colX': [7, 8, 9, 9],
    'colY': [10, 11, 12, 12],
})
new_df = (ChainDF(df)
            .select(['colA', 'colB']) # 列の抽出
            .calc_and_add_col_from_multi_cols(['colA', 'colB'], 'colC', add) # colA と colB の値を足して colC とする
            .value()) # pandas DataFrame をリターン
print(new_df)
'''
=>
   colA  colB  colC
0     1     4     5
1     2     5     7
2     3     6     9
3     3     6     9
'''
```


## 開発への参加について

### 基本方針
原則として、このリポジトリは個人でのメンテナンスを継続する予定です。(※ソースはオープン、開発はクローズドという体制をとります。)

知人のうち、このライブラリをメンテナンスしたい人がいれば個別で相談してください。

Fork などはライセンスに従って自由に行ってください。

不具合の報告や機能追加の要望は、Issue にて受け付けています。

### 開発者向けセットアップ

```bash
pip install .
```

リアルタイムに変更を反映する場合には、 `-e` オプションを付与してください。
    
```bash
pip install -e .
```

### Test

```bash
pytest
```