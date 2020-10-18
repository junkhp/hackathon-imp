# マスク除去AI

2020年10月17~18日に開催されたサポーターズ主催のオータムハッカソン用プロジェクト

## アプリ概要

2020年10月現在では，新型コロナウイルスの影響で外出時はマスクの着用が必須な世の中になってしまっています．感染対策をしながら旅行に行ったり，少人数の友達をランチをしたりして，その時の思い出をカメラに収めたとしてもマスクによって顔が半分も隠れてしまうなんてことがよくあるのではないでしょうか．

そこで今回は，以下のように**マスクをした人の画像からマスクを取り除き，口元を表現するアプリ**を作成しました！  
このアプリを使用して，思い出とその写真をぜひマスクから離れて保存しましょう！

| 変換前 | 変換後 |
| ---- | ---- |
| <img src="https://dl.dropboxusercontent.com/s/ynpe3gc730qa8fw/sample_before.jpg?dl=0" width="300"> | <img src="https://dl.dropboxusercontent.com/s/ha458caeh8p56os/sample_after.jpg?dl=0" width="300"> |

※ フリー画像を使用 (<a href="https://pixabay.com/ja/users/danieltwal-6963113/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=5178786">Daniel Twal</a>による<a href="https://pixabay.com/ja/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=5178786">Pixabay</a>からの画像)

## アプリ構造
<img src="https://dl.dropboxusercontent.com/s/nxaabelksszdk56/overview.png?dl=0" width="400">

## 使い方
ローカルのdocker上で環境を立ち上げる方法のみになります．  
今後，デプロイする予定です．

### dockerを使用する場合

- 環境構築済みのイメージをpullして，サーバーを起動する
  ```
  docker run -it -p 8099:8099 nh122112/rm-mask:v2.0 \
    /bin/bash /workspace/hackathon-imp/script/runserver.sh
  ```
  run後，ローカルのwebブラウザで `localhost:8099` にアクセス
- イメージのbuildも可能です．
  ```
  cd docker
  docker build ./ -t rm-mask:latest
  docker run -it -p 8099:8099 rm-mask:latest \
    /bin/bash /workspace/hackathon-imp/script/runserver.sh
  ```
