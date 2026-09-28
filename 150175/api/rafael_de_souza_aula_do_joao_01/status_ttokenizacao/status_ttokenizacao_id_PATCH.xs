// Edit STATUS _TTOKENIZACAO record
query "status_ttokenizacao/{status_ttokenizacao_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_ttokenizacao_id? filters=min:1
    dblink {
      table = "STATUS _TTOKENIZACAO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "STATUS _TTOKENIZACAO" {
      field_name = "id"
      field_value = $input.status_ttokenizacao_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $status_ttokenizacao
  }

  response = $status_ttokenizacao
  guid = "NHHSkYUUgtK0ejeySKV2GlOeMGg"
}