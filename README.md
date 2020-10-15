# hackathon-imp

サポーターズ主催のハッカソン用プロジェクト．


## Commands

### データベースの構築

```
python manage.py migrate
```

### サーバー立ち上げ
```
python manage.py runserver 0:8000
```


## Code

ビューは `rm_mask/view.py` 内で定義されている． それぞれの内容は以下の通りである．

- `IndexPageView`
  - 説明: 最初のページ．画像をアップロードする．
  - URL: /
  - POST の動作: 顔画像からマスク領域を推定．


- `MaskPageView`
  - 説明: 顔画像のマスク部分を調整するページ．
  - URL: /mask
  - POST の動作: マスク部分を白く塗ったあと画像変換．
  

- `ResultPageView`
  - 説明: 出力結果を表示するページ．
  - URL: /result


## Sessions

ウェブでは基本的にリクエストをまたいで変数の値を共有することはできない．しかし，セッションを使うとユーザーの入力などを保存しておくことができる．

- `request.session.image_path`: 入力画像の保存先
- `request.session.edge_positions`: マスク領域の頂点の座標
- `request.session.output_path`: 出力画像の保存先
