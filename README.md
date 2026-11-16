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

### Claude Code での確認の結果

Vault 2.2.2 (KV v2 を `kv/` に有効化) で、架空の 1 行を移行した。値の入力と Save のクリックは人間が行った。確認後に削除した。

| 確認 | 結果 |
|---|---|
| Bob 用のトークンでの接続の確認 (0 件のとき) | `404` |
| Bob 用のトークンでの値の読み取り・書き込み、移行先の外のパス | すべて `403` |
| `VAULT_TOKEN` が空のとき | `403` (SKILL.md に見分け方を記述) |
| 01 の `role=link[name="kv/"]` | 1 つに決まる |
| 02 の値の欄の名前 | キーを入力すると、そのキーの名前になる (`password`)。`masked input` は末尾の空の行に当たる。SKILL.md を修正 |
| 保存後の画面 | Overview タブが開き、値の行は出ない。03 は Secret タブを開いて撮影する。SKILL.md に操作を追加 |
| Secret タブ | 値は伏字で表示される。Delete・Destroy・Copy・JSON / YAML の切り替えがある |
| 保存後の API の一覧 | 名前が出る。メタデータは `200`、値は `403` |
| ログインした後のページの読み込み直し | ログインが消える。SKILL.md で `browser_navigate` を禁止 |

02 の黒塗りを利用者の指示で外す流れも、Claude Code (ツールなし、SKILL.md をシステムプロンプトに入れた別プロセス) で確認した。
最初の一覧で 02 を「値の欄は黒塗り」と書き、利用者が「黒塗りしない」と直すと「値の欄は黒塗りなし (利用者の指示)」に書き換えて再確認を求め、
`{ mask: "auto" }` は残し、値の欄の mask だけを付けなかった。spec の書き方は screenshot-for-bob の形にならなかったため、SKILL.md に 02 の spec の例を加えた。
例を加えた後、screenshot-for-bob の SKILL.md も一緒にシステムプロンプトに入れて、既定の場合と黒塗りを外した場合の 2 通りで 02 の撮影を依頼した。
どちらも `window.__sfbSpec = { out, items }` の形になり、外した場合は `{ mask: 'role=textbox[name="password"]' }` の 1 行だけが無く、`{ mask: "auto" }` は残った。
どちらも値の入力後に `browser_snapshot` と `browser_navigate` を使わなかった。

この確認では screenshot-for-bob を使っておらず、注釈と黒塗りの付いた画像は作成していない。Bob での確認で行う。

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
