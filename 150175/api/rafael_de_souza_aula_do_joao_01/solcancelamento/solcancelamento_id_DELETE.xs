// Delete SOLCANCELAMENTO record.
query "solcancelamento/{solcancelamento_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int solcancelamento_id? filters=min:1
  }

  stack {
    db.del SOLCANCELAMENTO {
      field_name = "id"
      field_value = $input.solcancelamento_id
    }
  }

  response = null
  guid = "ZyvbaXNk4IEt79ECPx4-hmJg5HQ"
}