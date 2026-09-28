// Add STATUS_CLIENTES record
query status_clientes verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "STATUS_CLIENTES"
    }
  }

  stack {
    db.add STATUS_CLIENTES {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_clientes
  }

  response = $status_clientes
  guid = "B2fo-kKlmkyZ_N2VJbwXbw58R38"
}