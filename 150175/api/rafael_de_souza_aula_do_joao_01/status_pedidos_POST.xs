// Add STATUS_PEDIDOS record
query status_pedidos verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "STATUS_PEDIDOS"
    }
  }

  stack {
    db.add STATUS_PEDIDOS {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_pedidos
  }

  response = $status_pedidos
  guid = "nXU1zPPmt01r4LjXfOks23pfObs"
}