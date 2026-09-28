// Delete STATUS_CLIENTE record.
query "status_cliente/{status_cliente_id}" verb=DELETE {
  api_group = "Rafael's Workspace"

  input {
    int status_cliente_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_cliente_id
    }
  }

  response = null
  guid = "EQIS0dBAah1MlX3Nh6vXMYYvot8"
}