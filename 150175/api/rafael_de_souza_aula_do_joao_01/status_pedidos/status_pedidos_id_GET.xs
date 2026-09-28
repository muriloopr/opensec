// Get STATUS_PEDIDOS record
query "status_pedidos/{status_pedidos_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_pedidos_id? filters=min:1
  }

  stack {
    db.get STATUS_PEDIDOS {
      field_name = "id"
      field_value = $input.status_pedidos_id
    } as $status_pedidos
  
    precondition ($status_pedidos != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_pedidos
  guid = "V8BmUaLQjF1xYJx-h1EJOASCfOI"
}