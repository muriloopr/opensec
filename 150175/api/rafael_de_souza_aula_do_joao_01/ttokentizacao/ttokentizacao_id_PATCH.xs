// Edit TTOKENTIZACAO record
query "ttokentizacao/{ttokentizacao_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int ttokentizacao_id? filters=min:1
    dblink {
      table = "TTOKENTIZACAO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch TTOKENTIZACAO {
      field_name = "id"
      field_value = $input.ttokentizacao_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $ttokentizacao
  }

  response = $ttokentizacao
  guid = "Qs3d7Hjk5v7_MjKISFAflRc0CqU"
}