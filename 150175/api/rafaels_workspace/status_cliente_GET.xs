// Query all STATUS_CLIENTE records
query status_cliente verb=GET {
  api_group = "Rafael's Workspace"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_cliente
  }

  response = $status_cliente
  guid = "6LNSQ56OC_C7oWtm-fHxvMZTscI"
}