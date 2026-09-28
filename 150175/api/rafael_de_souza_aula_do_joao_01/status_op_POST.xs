// Add STATUS_OP record
query status_op verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "STATUS_OP"
    }
  }

  stack {
    db.add STATUS_OP {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_op
  }

  response = $status_op
  guid = "xBQAxLumEAQi0Ffq0YWj5l86Zj4"
}