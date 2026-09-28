// Get TOKENS record
query "tokens/{tokens_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int tokens_id? filters=min:1
  }

  stack {
    db.get TOKENS {
      field_name = "id"
      field_value = $input.tokens_id
    } as $tokens
  
    precondition ($tokens != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $tokens
  guid = "87K0Sl-5Xa26NKPoVPvj66pmZWs"
}