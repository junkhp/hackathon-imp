# estimate mask edge positions
マスクを着用した自撮り画像を入力として，マスクの境界位置を推定するスクリプト．

## しくみ
[RetinaFaceのマスク対応版](https://github.com/deepinsight/insightface/tree/master/RetinaFaceAntiCov)(RetinaFaceAntiCov)で顔検出，5点ランドマークを推定し，それらの情報を元に幾何的にマスク位置を推定する．

## 使い方

### RetinaFaceAntiCovの準備

1.  RetinaFaceAntiCov本体を[ここ](https://github.com/deepinsight/insightface/tree/master/RetinaFaceAntiCov)からもってきてこのディレクトリに配置

2. 何故かコードが不足しているので，RetinaFaceの[rcnn/cythonディレクトリ](https://github.com/deepinsight/insightface/tree/master/RetinaFace/rcnn/cython)を`RetinaFaceAnticov/rcnn/`にコピー

3. RetinaFaceの動作に必要なライブラリのインストール

```
pip install mxnet cython
```

4. RetinaFaceAnticov/rcnn/cython ディレクトリに移動し，cython関係のモジュールをコンパイル (うまくコンパイルできるように祈ろう)
```
python setup.py build_ext --inplace
```

5. 最後に，RetinaFaceAntiCovにmodelディレクトリを作成，学習済みモデルを[RetinaFaceAntiCovのページ](https://github.com/deepinsight/insightface/tree/master/RetinaFaceAntiCov)から拝借し，`RetinaFaceAntiCov/model`に設置して，準備完了．


### マスク境界位置推定スクリプトの仕様
- estimate_mask_edge_positions.py
    - *function* estimate_mask_edge_positions ( *image_path* )

        画像のパスを入力として，マスクの境界位置(edge positions)を8点で推定します．
    
        境界位置を構成する点は，1番目の点が鼻の部分，以降は鼻の部分を基準に時計回りになっています．
        
        顔検出器が複数の顔を検出した場合は，検出に成功した顔の中で最も大きい顔の輪郭を返します．また，顔の検出に失敗した場合は*None*を返します．