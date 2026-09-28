// Query all STATUS _TTOKENIZACAO records
query status_ttokenizacao verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query "STATUS _TTOKENIZACAO" {
      return = {type: "list"}
    } as $status_ttokenizacao
  }

  response = $status_ttokenizacao
  guid = "w5WWpaghOrgSdg0LfqBkomZHuzo"
}