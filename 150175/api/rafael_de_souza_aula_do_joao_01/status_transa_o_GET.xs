// Query all STATUS_TRANSAÇÃO records
query status_transa_o verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query "STATUS_TRANSAÇÃO" {
      return = {type: "list"}
    } as $status_transa_o
  }

  response = $status_transa_o
  guid = "D_WI6IdLQVTeosMHClJgC145FbA"
}