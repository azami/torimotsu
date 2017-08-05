# TORIMOTSU

## 概要

fitbit APIから昨日食べたものを取得し、Slackに通知する。

## 必要な設定

- fitibit APIのtoken設定
    - 適宜更新するので、TORIMOTSUから書き込みができること
    - [fitbit API OAuth2.0チュートリアルページ](https://dev.fitbit.com/apps/oauthinteractivetutorial)の `Authorization Code Flow` で認証してtoken、refresh tokenを取得し、 `Get Code` のレスポンスをリポジトリのroodディレクトリの `.token.json` に保存する。
    - 必要なScopeは `nutrition` `weight`
        - `weight` は今は使っていないけどそのうち。

- その他の設定
    - リポジトリのrootディレクトリに `settings.yml` をおく
    - 内容は `settings_sample.yml` を参考にする

## 使い方

- 環境
    - make、dockerが必要

```sh
make run
```

## 既知のバグ

- 日時がUTC固定
    - fitibit APIの仕様によるもの。いまのところなおす気はない。