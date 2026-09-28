// Query all STATUS_PEDIDOS records
query status_pedidos verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query STATUS_PEDIDOS {
      return = {type: "list"}
    } as $status_pedidos
  }

  response = $status_pedidos
  guid = "SdBq3JS7IX_1SF89EHhu2kXma1s"
}