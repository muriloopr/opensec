// Get PAPEL record
query "papel/{papel_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int papel_id? filters=min:1
  }

  stack {
    db.get PAPEL {
      field_name = "id"
      field_value = $input.papel_id
    } as $papel
  
    precondition ($papel != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $papel
  guid = "nz-BLkRWUDsRt6K4W3ycwvnezDc"
}