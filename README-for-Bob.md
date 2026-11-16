# vault-for-bob: Bob の案内でパスワード一覧を Vault に移行する

IBM Bob が、HashiCorp Vault (KV v2) の Web UI の操作を 1 操作ずつ案内するスキルです。
Excel や CSV の共有のパスワード一覧の行を Vault のシークレットに移行し、
[screenshot-for-bob](https://github.com/unnowataru/screenshot-for-bob) と組み合わせて手順書の画像も作成します。

## 特徴

- **パスワードの値は人間が入力します。** Bob が読み込むのはサーバー名・用途・ユーザーの列だけです。値の欄への入力と保存のクリックは人間が行います
- **移行できたかは API で確認します。** Bob は一覧の取得だけができるトークンで、移行先にその名前があるかを確認します。値は読めません
- **手順書の画像を撮影します。** Secrets engines の一覧・作成画面・保存後・移行先の一覧の 4 枚を、注釈と黒塗りを付けて保存します

## 前提条件

- Vault (KV v2 のシークレットエンジンが有効) と、Web UI にログインできるアカウント
- Bob に Playwright MCP が接続されていること (設定は screenshot-for-bob の README-for-Bob.md を参照)
- Playwright MCP の設定で、ブラウザーが CSP を無視するようにしてあること (下記)。Vault の Web UI は CSP が厳しく、
  この設定が無いと、screenshot-for-bob が注釈を入れるためにページを読み込み直し、そのたびに Vault のログインが消えます
- 手順書の画像を撮影する場合は screenshot-for-bob
- Bob 用の Vault のトークン。移行先の一覧の取得だけを許可する policy を付けます (例: [`examples/policy-bob-list.hcl`](examples/policy-bob-list.hcl))

Bob 用のトークンは、Vault の管理者が次のように作成します (マウントが `kv/` の場合)。

```bash
vault policy write bob-list examples/policy-bob-list.hcl
vault token create -policy=bob-list -ttl=8h -display-name=bob
```

Playwright MCP の設定ファイル (例: `C:\Users\<ユーザー名>\.bob\settings\playwright-mcp-config.json`) を作成します。

```json
{
  "browser": {
    "contextOptions": { "bypassCSP": true }
  }
}
```

Bob の `mcp.json` の playwright の `args` に、`"--config"` とこのファイルのパスを追加します。この設定は Bob の Playwright のブラウザーにだけ効き、
普段使うブラウザーには影響しません。`--isolated` (専用のプロファイル) と組み合わせて使うことをお勧めします。

## 入れ方

1. `vault-for-bob` フォルダーを次の場所に配置します
   - どのワークスペースでも使う場合: `C:\Users\<ユーザー名>\.bob\skills\vault-for-bob`
   - 特定のフォルダーだけで使う場合: そのフォルダーの `.bob\skills\vault-for-bob`
2. Bob のすべてのウィンドウを閉じて終了し、環境変数 `VAULT_ADDR` (例: `https://vault.example.internal:8200`) と `VAULT_TOKEN` (Bob 用のトークン) を設定したシェルから Bob を起動します。
   Bob のウィンドウが 1 つでも残っていると、新しく起動した Bob は既存のプロセスに引き継がれ、環境変数が届きません

## 使い方の例

移行元の一覧から、パスワードの列を除いた CSV のファイルを用意し、Bob のワークスペースに置きます
(例: [`examples/servers.csv`](examples/servers.csv) のパスワードの列を削除したもの)。
Excel の一覧は、パスワードの列を削除してから CSV で保存します。

次のプロンプトを、上から順に Bob のチャットに入力します。URL・ファイル名・移行先のパスは、環境に合わせて書き換えます。

### 1. Vault の Web UI を開く

```text
Playwright で https://vault.example.internal:8200/ui/ を開いて。ログインは私がするので、「ログインした」と言うまで何もしないで待って。
```

Bob が開いたブラウザーで、Vault にログインします。ログインした後は、ページを読み込み直さないでください。

### 2. 移行を依頼する

```text
ログインした。
サーバーの一覧 (servers.csv の サーバー名・用途・ユーザー の列) を Vault の kv/servers/ に移行したい。
今回は web-01 の 1 行だけでいい。
vault-for-bob で 1 操作ずつ案内して、screenshot-for-bob で手順書の画像も screenshots/ に作成して。
値の入力と Save のクリックは私が行う。
```

Bob が移行の一覧と撮影の一覧を提示します。内容を確認して `OK` と返します。

### 3. 案内に従って操作する

Bob が 1 操作ずつ案内します。操作が終わるたびに次のように返します。

```text
できた
```

パスワードの値の入力と Save のクリックは、Bob が案内したときに人間が行います。Bob が撮影を終えるまで、Save はクリックしません。

### デモ用のダミーの値で、02 の値の欄を黒塗りしない場合

撮影の一覧の確認で、次のように返します。本番の値では使いません。

```text
02 の値の欄はデモ用のダミーの値なので、黒塗りしなくていい。
```

### 2 行目以降

1 行目と同じ流れで、撮影はしません。

```text
続けて db-01 と backup-01 も移行したい。撮影は不要。
```

## 注意点

- **パスワードの列を Bob に渡さないでください。** Bob は読み込む列を確認してから読み込みますが、ファイルを渡す前に列を除いておくのが確実です
- **Bob 用のトークンに、値を読む権限を付けないでください。** スキルの文面だけでは、Bob が値を読む操作を防げません。防ぐのは policy です
- **撮影した画像は必ず開いて確認してください。** 値の欄は黒塗りしますが、漏れは自動では見つけられません
- **ログインした後、ブラウザーのページを読み込み直さないでください。** Vault の UI はログインが消えます
- Bob Shell の `bob run` (対話しない実行) では使わないでください。人間が値を入力する場面がありません

## 外し方

`vault-for-bob` フォルダーを削除します。Bob 用のトークンは `vault token revoke` で無効にします。
