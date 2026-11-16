# Bob 用のトークンに付ける policy の例。
# 移行先 (kv/servers/) の一覧とメタデータの読み取りだけを許可する。値 (kv/data/...) は読めない。
# マウントが kv/ 以外なら、パスの先頭を書き換える。

# 一覧 (vault kv list kv/servers、LIST /v1/kv/metadata/servers/)
path "kv/metadata/servers/" {
  capabilities = ["list"]
}

# 各シークレットのメタデータ (版の数・作成日時など。値は含まない)
path "kv/metadata/servers/*" {
  capabilities = ["list", "read"]
}
