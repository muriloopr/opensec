// Get TTOKENTIZACAO record
query "ttokentizacao/{ttokentizacao_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int ttokentizacao_id? filters=min:1
  }

  stack {
    db.get TTOKENTIZACAO {
      field_name = "id"
      field_value = $input.ttokentizacao_id
    } as $ttokentizacao
  
    precondition ($ttokentizacao != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $ttokentizacao
  guid = "wnBP-G_rkv9oe3qCzwrYQdchZVs"
}