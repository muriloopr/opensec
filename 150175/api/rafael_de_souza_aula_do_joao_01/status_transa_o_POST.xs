// Add STATUS_TRANSAÇÃO record
query status_transa_o verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "STATUS_TRANSAÇÃO"
    }
  }

  stack {
    db.add "STATUS_TRANSAÇÃO" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_transa_o
  }

  response = $status_transa_o
  guid = "Chmfar2nIMQc2aA21KzpJUTdLac"
}