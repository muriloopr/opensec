// Get STATUS_CLIENTES record
query "status_clientes/{status_clientes_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_clientes_id? filters=min:1
  }

  stack {
    db.get STATUS_CLIENTES {
      field_name = "id"
      field_value = $input.status_clientes_id
    } as $status_clientes
  
    precondition ($status_clientes != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_clientes
  guid = "xSJ2avhfEyL8p6sovdvnz9rwJVA"
}