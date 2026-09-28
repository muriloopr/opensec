// Edit STATUS_TRANSAÇÃO record
query "status_transa_o/{status_transa_o_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_transa_o_id? filters=min:1
    dblink {
      table = "STATUS_TRANSAÇÃO"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "STATUS_TRANSAÇÃO" {
      field_name = "id"
      field_value = $input.status_transa_o_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $status_transa_o
  }

  response = $status_transa_o
  guid = "68hBVBMJcyXEGni3SF5BfLg-wYQ"
}