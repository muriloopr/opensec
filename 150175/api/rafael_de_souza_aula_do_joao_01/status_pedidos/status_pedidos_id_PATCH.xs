// Edit STATUS_PEDIDOS record
query "status_pedidos/{status_pedidos_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_pedidos_id? filters=min:1
    dblink {
      table = "STATUS_PEDIDOS"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch STATUS_PEDIDOS {
      field_name = "id"
      field_value = $input.status_pedidos_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $status_pedidos
  }

  response = $status_pedidos
  guid = "tUtMD-XrtJqzAUIhEQyfyNt2wFw"
}