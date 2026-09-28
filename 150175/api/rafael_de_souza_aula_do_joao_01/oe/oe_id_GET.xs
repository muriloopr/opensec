// Get OE record
query "oe/{oe_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int oe_id? filters=min:1
  }

  stack {
    db.get OE {
      field_name = "id"
      field_value = $input.oe_id
    } as $oe
  
    precondition ($oe != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $oe
  guid = "5vYjeD1KDr4ugSh5UOI8qtC-jBA"
}