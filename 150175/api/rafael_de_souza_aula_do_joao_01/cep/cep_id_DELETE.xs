// Delete CEP record.
query "cep/{cep_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int cep_id? filters=min:1
  }

  stack {
    db.del CEP {
      field_name = "id"
      field_value = $input.cep_id
    }
  }

  response = null
  guid = "TC1mZ8HMG51UuoqSJSTmxbkau4o"
}