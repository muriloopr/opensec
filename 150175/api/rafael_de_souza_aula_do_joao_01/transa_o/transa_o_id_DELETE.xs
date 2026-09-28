// Delete TRANSAÇÃO record.
query "transa_o/{transa_o_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int transa_o_id? filters=min:1
  }

  stack {
    db.del "TRANSAÇÃO" {
      field_name = "id"
      field_value = $input.transa_o_id
    }
  }

  response = null
  guid = "jANoLsmQlezgAx9V7nZrfqygqYA"
}