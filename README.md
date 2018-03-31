# 任意の画像を組み合わせたパズルを作成できるアプリ

## Development

dockerをインストールしておくこと  

### clone

```bash
$ git clone https://github.com/StudioAquatan/kit_campus_puzzle.git
```

### 起動

まずは`build`する

```bash
$ cd kit_campus_puzzle
$ pwd
/path/to/kit_campus_puzzle
$ docker-compose build
```


ビルドが正常に成功したら`docker/**/.env`ファイルを編集し、適切な値を入力して、`up`してコンテナを起動

```bash
$ docker-compose up
```

`docker ps`してDjangoアプリケーションが動いているコンテナ名を取得し、migrate及びcreatesuperuserする

```bash
$ docker exec -it {{ コンテナ名 }} python3 manage.py migrate && python3 manage.py createsuperuser
```

`http://127.0.0.1/admin`へアクセスする

