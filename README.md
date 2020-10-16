# hackathon-imp

サポーターズ主催のハッカソン用プロジェクト．


## Commands

### データベースの構築

```
python manage.py migrate
```

### サーバー立ち上げ
```
python manage.py runserver
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

## 追加機能  
ファイル名と関数名を明示的にするための一覧  
もし，/rm_mask 以下にdirectoryを作りたい場合は，そのようにしてくれてもOK  
（むしろ，その方がよいかも）
- generate_masked_image.py  
  - generate_masked_image()  
    マスクの座標からマスク部分を白くした画像を保存し，その画像のパスを返す  
    （もし可能なら，ここに処理の流れを簡単に書いておくと他の人にもわかりやすいかも）
    ~~~
    args:
      image_path: 変換対象の画像が保存されている絶対パス
      edge_positions: マスクの境界を示す座標
    return:
      masked_image_path: マスク部分を白くした画像の絶対パス
    ~~~
- inpainting.py
  - inpaint_masked_image()  
    マスク部分を白くした画像をpix2pixでinpaintingし，その画像のパスを返す
    ~~~
    args:
      masked_image_path: マスク部分を白くした画像の絶対パス
    return:
      inpainted_image_path: マスク部分を人の口元に変換した画像の絶対パス
    ~~~

## Sessions

ウェブでは基本的にリクエストをまたいで変数の値を共有することはできない．しかし，セッションを使うとユーザーの入力などを保存しておくことができる．

- `request.session['image_path']`: 入力画像の保存先
- `request.session['edge_positions']`: マスク領域の頂点の座標
- `request.session['output_path']`: 出力画像の保存先
