# my-class-pdf
フォルダ内のpdfをブラウザから一覧するだけのアプリ

時間によって開くフォルダが自動で変わる

## 使い方

* 必要なパッケージ: flaskとmarkdownのインストール(またはpipenvを使ってる人はPipfileを使用)

```bash
pip3 install flask markdown
```

* pythonで`import tkinter`が使えることを確認(参考: https://stackoverflow.com/questions/63643687/import-tkinter-if-this-fails-your-python-may-not-be-configured-for-tk-error-i)
* サーバー起動(pipenvでは`pipenv run start`)
  * macだとデフォルトの5000は使えないっぽいので8000を指定した

```bash
flask run --port 8000
```

* ブラウザで http://127.0.0.1:8000/ を開く
  * タブとして開いて使えるが、Vivaldiだったらパネルに登録すると便利
