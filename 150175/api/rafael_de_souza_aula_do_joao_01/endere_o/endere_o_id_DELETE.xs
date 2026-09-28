// Delete ENDEREÇO record.
query "endere_o/{endere_o_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int endere_o_id? filters=min:1
  }

  stack {
    db.del "ENDEREÇO" {
      field_name = "id"
      field_value = $input.endere_o_id
    }
  }

  response = null
  guid = "KI8F_-zA0GtOKG2eLKDz24mz260"
}