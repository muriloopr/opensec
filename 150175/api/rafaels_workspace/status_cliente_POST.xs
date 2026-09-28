// Add STATUS_CLIENTE record
query status_cliente verb=POST {
  api_group = "Rafael's Workspace"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_cliente
  }

  response = $status_cliente
  guid = "9Cp6oVzvhq8eTWk6rl3k6h80biA"
}