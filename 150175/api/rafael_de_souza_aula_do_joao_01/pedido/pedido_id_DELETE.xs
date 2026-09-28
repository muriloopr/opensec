// Delete PEDIDO record.
query "pedido/{pedido_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int pedido_id? filters=min:1
  }

  stack {
    db.del PEDIDO {
      field_name = "id"
      field_value = $input.pedido_id
    }
  }

  response = null
  guid = "aSnEA_KW9UXWw9tJtC8No9EDHJk"
}