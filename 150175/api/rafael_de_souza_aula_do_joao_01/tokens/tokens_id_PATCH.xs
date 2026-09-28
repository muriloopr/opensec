// Edit TOKENS record
query "tokens/{tokens_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int tokens_id? filters=min:1
    dblink {
      table = "TOKENS"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch TOKENS {
      field_name = "id"
      field_value = $input.tokens_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $tokens
  }

  response = $tokens
  guid = "6P8fp8Rd1yCMRx1wlAH0HrizYA0"
}