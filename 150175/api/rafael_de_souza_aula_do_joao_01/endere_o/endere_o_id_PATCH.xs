// Edit ENDEREÇO record
query "endere_o/{endere_o_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int endere_o_id? filters=min:1
    dblink {
      table = "ENDEREÇO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "ENDEREÇO" {
      field_name = "id"
      field_value = $input.endere_o_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $endere_o
  }

  response = $endere_o
  guid = "s-R4D3aJzjFaOmi3_wxd8wS7wRw"
}