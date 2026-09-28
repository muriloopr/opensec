// Query all PEDIDO records
query pedido verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query PEDIDO {
      return = {type: "list"}
    } as $pedido
  }

  response = $pedido
  guid = "ayx0AUbxQTZG_9mbySBbRkX77YE"
}