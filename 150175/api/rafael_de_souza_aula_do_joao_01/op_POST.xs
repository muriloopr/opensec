// Add OP record
query op verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "OP"
    }
  }

  stack {
    db.add OP {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $op
  }

  response = $op
  guid = "89TpIlRiJWTpKOrDpFIokKvzX-c"
}