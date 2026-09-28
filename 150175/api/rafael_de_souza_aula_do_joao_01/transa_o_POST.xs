// Add TRANSAÇÃO record
query transa_o verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "TRANSAÇÃO"
    }
  }

  stack {
    db.add "TRANSAÇÃO" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $transa_o
  }

  response = $transa_o
  guid = "v_vuq56h-NC9nH5m1CAfNFbZzks"
}