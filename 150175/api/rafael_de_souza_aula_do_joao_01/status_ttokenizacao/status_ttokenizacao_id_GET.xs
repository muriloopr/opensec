// Get STATUS _TTOKENIZACAO record
query "status_ttokenizacao/{status_ttokenizacao_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_ttokenizacao_id? filters=min:1
  }

  stack {
    db.get "STATUS _TTOKENIZACAO" {
      field_name = "id"
      field_value = $input.status_ttokenizacao_id
    } as $status_ttokenizacao
  
    precondition ($status_ttokenizacao != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_ttokenizacao
  guid = "PRC9Zxe3KBnhOxemFEwLr8dGVRI"
}