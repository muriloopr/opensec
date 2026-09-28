// Get ENDEREÇO record
query "endere_o/{endere_o_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int endere_o_id? filters=min:1
  }

  stack {
    db.get "ENDEREÇO" {
      field_name = "id"
      field_value = $input.endere_o_id
    } as $endere_o
  
    precondition ($endere_o != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $endere_o
  guid = "2MiD59BVjDMwoFbhTTNwBJIy0ls"
}