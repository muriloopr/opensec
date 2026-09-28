// Delete STATUS _TTOKENIZACAO record.
query "status_ttokenizacao/{status_ttokenizacao_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_ttokenizacao_id? filters=min:1
  }

  stack {
    db.del "STATUS _TTOKENIZACAO" {
      field_name = "id"
      field_value = $input.status_ttokenizacao_id
    }
  }

  response = null
  guid = "DEkgCbNjY6_8gxSS2wHj2XKPmDM"
}