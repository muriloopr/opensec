// Delete STATUS_CLIENTES record.
query "status_clientes/{status_clientes_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_clientes_id? filters=min:1
  }

  stack {
    db.del STATUS_CLIENTES {
      field_name = "id"
      field_value = $input.status_clientes_id
    }
  }

  response = null
  guid = "Su_YzI3q4hmX0jn8cK-1OhLAzSQ"
}