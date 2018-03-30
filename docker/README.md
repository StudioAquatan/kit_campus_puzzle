# 任意の画像を組み合わせたパズルを作成できるアプリ

## Development

dockerをインストールしておくこと  

### データベースの起動

```bash
$ docker-compose up db
```

### パラメータの入力

```bash
$ cp docker/app/.env.sample docker/app/.env
$ cp docker/mysql/.env.sample docker/mysql/.env
```

それぞれ編集する

