# my-class-pdf
フォルダ内のpdfをブラウザから一覧するだけのアプリ

時間によって開くフォルダが自動で変わる

## 使い方

* 必要なパッケージのインストール
  * またはpipenvを使ってる人はPipfileを使用

```bash
pip3 install flask markdown
```

* サーバー起動
  * macだとデフォルトの5000は使えないっぽいので以下のように適当なポートを指定

```bash
flask run --port 8000
```

* ブラウザで http://127.0.0.1:8000/ を開く
  * Vivaldiのパネルとかに登録すると便利
