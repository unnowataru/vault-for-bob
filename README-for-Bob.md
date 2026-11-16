# vault-for-bob: Bob の案内でパスワード一覧を Vault に移行する

IBM Bob が、HashiCorp Vault (KV v2) の Web UI の操作を 1 操作ずつ案内するスキルです。
共有のパスワード一覧 (Excel・CSV) の行を Vault のシークレットに移行し、
[screenshot-for-bob](https://github.com/unnowataru/screenshot-for-bob) と組み合わせて手順書の画像も作成します。

## 特徴

- **パスワードの値は人間が入力します。** Bob が読み込むのはサーバー名・用途・ユーザーの列だけです。値の欄への入力と保存のクリックは人間が行います
- **移行できたかは API で確認します。** Bob は一覧の取得だけができるトークンで、移行先にその名前があるかを確認します。値は読めません
- **手順書の画像を撮影します。** Secrets engines の一覧・作成画面・保存後・移行先の一覧の 4 枚を、注釈と黒塗りを付けて保存します

## 前提条件

- Vault (KV v2 のシークレットエンジンが有効) と、Web UI にログインできるアカウント
- Bob に Playwright MCP が接続されていること (設定は screenshot-for-bob の README-for-Bob.md を参照)
- 手順書の画像を撮影する場合は screenshot-for-bob
- Bob 用の Vault のトークン。移行先の一覧の取得だけを許可する policy を付けます (例: [`examples/policy-bob-list.hcl`](examples/policy-bob-list.hcl))

Bob 用のトークンは、Vault の管理者が次のように作成します (マウントが `kv/` の場合)。

```bash
vault policy write bob-list examples/policy-bob-list.hcl
vault token create -policy=bob-list -ttl=8h -display-name=bob
```

## 入れ方

1. `vault-for-bob` フォルダーを次の場所に配置します
   - どのワークスペースでも使う場合: `C:\Users\<ユーザー名>\.bob\skills\vault-for-bob`
   - 特定のフォルダーだけで使う場合: そのフォルダーの `.bob\skills\vault-for-bob`
2. Bob を起動する前に、環境変数 `VAULT_ADDR` (例: `https://vault.example.internal:8200`) と `VAULT_TOKEN` (Bob 用のトークン) を設定します
3. Bob を開き直します

## 使い方の例

1. Playwright MCP のブラウザーで Vault の Web UI を開き、ログインしておきます
2. 移行元の一覧から、パスワードの列を除いたファイルを用意します (例: [`examples/servers.csv`](examples/servers.csv) のパスワードの列を削除したもの)
3. Bob のチャットで、次のように依頼します

> サーバーの一覧 (servers.csv の サーバー名・用途・ユーザー の列) を Vault の kv/servers/ に移行したい。
> vault-for-bob で 1 操作ずつ案内して、screenshot-for-bob で手順書の画像も screenshots/ に作成して。

Bob が移行の一覧と撮影の一覧を提示するので、確認してから進めます。値の入力と Save のクリックは、案内に従って人間が行います。

## 注意点

- **パスワードの列を Bob に渡さないでください。** Bob は読み込む列を確認してから読み込みますが、ファイルを渡す前に列を除いておくのが確実です
- **Bob 用のトークンに、値を読む権限を付けないでください。** スキルの文面だけでは、Bob が値を読む操作を防げません。防ぐのは policy です
- **撮影した画像は必ず開いて確認してください。** 値の欄は黒塗りしますが、漏れは自動では見つけられません
- **ログインした後、ブラウザーのページを読み込み直さないでください。** Vault の UI はログインが消えます
- Bob Shell の `bob run` (対話しない実行) では使わないでください。人間が値を入力する場面がありません

## 外し方

`vault-for-bob` フォルダーを削除します。Bob 用のトークンは `vault token revoke` で無効にします。
