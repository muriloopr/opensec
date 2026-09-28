// Edit CEP record
query "cep/{cep_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int cep_id? filters=min:1
    dblink {
      table = "CEP"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch CEP {
      field_name = "id"
      field_value = $input.cep_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $cep
  }

  response = $cep
  guid = "9zvugxf_X3HN_e8Aawxg-aGNUpY"
}