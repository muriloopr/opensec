// Add PEDIDO record
query pedido verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "PEDIDO"
    }
  }

  stack {
    db.add PEDIDO {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $pedido
  }

  response = $pedido
  guid = "NUR_LRIO4nXUm_LzoAtSCZ_iuDk"
}