// Add CLIENTE record
query cliente verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "CLIENTE"
    }
  }

  stack {
    db.add CLIENTE {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $cliente
  }

  response = $cliente
  guid = "0_vPRut9kwHcNhebwX4OtTFwfEU"
}