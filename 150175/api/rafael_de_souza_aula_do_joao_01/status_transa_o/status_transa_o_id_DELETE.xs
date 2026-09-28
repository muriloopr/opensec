// Delete STATUS_TRANSAÇÃO record.
query "status_transa_o/{status_transa_o_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_transa_o_id? filters=min:1
  }

  stack {
    db.del "STATUS_TRANSAÇÃO" {
      field_name = "id"
      field_value = $input.status_transa_o_id
    }
  }

  response = null
  guid = "BgX3cUK0P58LIzbYUH-0fFuN3Kk"
}