// Query all STATUS_CLIENTES records
query status_clientes verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query STATUS_CLIENTES {
      return = {type: "list"}
    } as $status_clientes
  }

  response = $status_clientes
  guid = "WTH1erCkhraW7awuoO6YKnjD2cA"
}