# vault-for-bob

IBM Bob (IDE / Bob Shell) 用のスキル。HashiCorp Vault (KV v2) の Web UI の操作を人間に 1 操作ずつ案内し、
共有のパスワード一覧の行を KV に移行する。移行できたかは Vault の API (一覧の取得だけ) で確認する。
手順書の画像の撮影は [screenshot-for-bob](https://github.com/unnowataru/screenshot-for-bob) に任せる。
利用者向けの説明は [README-for-Bob.md](README-for-Bob.md)、Bob への手順は [SKILL.md](SKILL.md)。

## 構成

| ファイル | 内容 |
|---|---|
| `SKILL.md` | Bob への手順。守ること・流れ・撮影の一覧・画面の要素の名前 |
| `README-for-Bob.md` | 利用者向けの説明 |
| `examples/policy-bob-list.hcl` | Bob 用のトークンの policy の例 (一覧とメタデータの読み取りだけ) |
| `examples/servers.csv` | 試験用の架空の一覧 |
| `tools/package.py` | 配布用の zip を作成する |

## 役割分担の考え方

| 操作 | 担当 | 理由 |
|---|---|---|
| パスワードの値の入力 | 人間 (UI) | 値が Bob の入力・コマンド・ログを通らないようにする |
| 保存 (Save) のクリック | 人間 (UI) | 変更の確定は人間が行う |
| 画面の移動 | 人間 (UI) | Vault の UI はページを読み込み直すとログインが消えるため、Bob は `browser_navigate` を使わない |
| 移行できたかの確認 | Bob (API) | 一覧の取得だけの権限で確認する。値は読めない |
| 撮影 | Bob (screenshot-for-bob) | 注釈と黒塗りを撮影の前に入れる |

## 動作確認

### Claude Code での確認

スキルの文面どおりに進むかを、Claude Code にこのフォルダーを読み込ませて確認する。Bob で通る保証にはならない。

1. テスト用の Vault を用意する (本番の Vault は使わない)。KV v2 を `kv/` に有効化し、`examples/policy-bob-list.hcl` の policy とトークンを作成する
2. `VAULT_ADDR` と `VAULT_TOKEN` (Bob 用のトークン) を設定して Claude Code を起動し、SKILL.md を読ませて、README-for-Bob.md の依頼文で依頼する
3. 次を確認する
   - 読み込む列の確認を求め、パスワードの列を読み込まない
   - 移行の一覧と撮影の一覧を提示して確認を求める
   - API での接続の確認が `404` か `200` になる
   - Bob 用のトークンで `kv/data/` を読むと `403` になる (policy の確認)
   - 人間が UI で 1 行を保存した後、API の一覧にその名前が出る
   - 完了の報告に値が含まれない

### Bob での確認

配布するのは、Bob で確認した版だけ。確認した版にタグを付ける。

1. `python tools/package.py` で zip を作成し、展開した `vault-for-bob` フォルダーを `~/.bob/skills/` に配置する。screenshot-for-bob も配置する
2. テスト用の Vault と Bob 用のトークンを用意し、`VAULT_ADDR` と `VAULT_TOKEN` を設定してから Bob を起動する
3. Playwright MCP のブラウザーで Vault の UI にログインする
4. README-for-Bob.md の依頼文で依頼し、`examples/servers.csv` からパスワードの列を除いた一覧で 1 行だけ移行する
5. Claude Code での確認と同じ項目に加え、次を確認する
   - Bob がスキルを選ぶか (依頼文でスキルの名前を挙げたとき、挙げないとき)
   - Bob のツールの承認の画面で、Vault の API を呼び出すコマンドにトークンの値が書かれていない
   - 撮影した 4 枚で、02 の値の欄が黒塗りされている
   - 承認の回数と、1 行にかかる時間
6. 確認に使った Bob の版、Vault の版、Playwright MCP の版を記録してタグを付ける (`git tag v<バージョン>`)

## 配布

```bash
python tools/package.py
```

`dist/vault-for-bob.zip` ができる (`dist/` は Git の管理外)。GitHub の Releases に添付して配る。

## ライセンス

MIT License ([LICENSE](LICENSE))。
