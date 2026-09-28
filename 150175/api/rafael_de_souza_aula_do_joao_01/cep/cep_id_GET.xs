// Get CEP record
query "cep/{cep_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int cep_id? filters=min:1
  }

  stack {
    db.get CEP {
      field_name = "id"
      field_value = $input.cep_id
    } as $cep
  
    precondition ($cep != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $cep
  guid = "OtUw1Lw0_o_D0SH_I3Q3GlHS3mg"
}