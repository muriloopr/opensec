// Delete CLIENTE record.
query "cliente/{cliente_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int cliente_id? filters=min:1
  }

  stack {
    db.del CLIENTE {
      field_name = "id"
      field_value = $input.cliente_id
    }
  }

  response = null
  guid = "ex7WjoMlaNlm3dzBRDVB6zF1Tw8"
}