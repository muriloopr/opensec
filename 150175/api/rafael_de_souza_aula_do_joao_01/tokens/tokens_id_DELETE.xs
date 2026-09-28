// Delete TOKENS record.
query "tokens/{tokens_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int tokens_id? filters=min:1
  }

  stack {
    db.del TOKENS {
      field_name = "id"
      field_value = $input.tokens_id
    }
  }

  response = null
  guid = "RYwe9nFQH4e2ZbPCx7RBqP4eo3s"
}