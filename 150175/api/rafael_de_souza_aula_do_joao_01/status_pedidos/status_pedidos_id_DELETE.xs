// Delete STATUS_PEDIDOS record.
query "status_pedidos/{status_pedidos_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_pedidos_id? filters=min:1
  }

  stack {
    db.del STATUS_PEDIDOS {
      field_name = "id"
      field_value = $input.status_pedidos_id
    }
  }

  response = null
  guid = "oNiIgpKpDjMKME4I3MBJkKr5OBk"
}