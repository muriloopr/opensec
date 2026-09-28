// Add CEP record
query cep verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "CEP"
    }
  }

  stack {
    db.add CEP {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $cep
  }

  response = $cep
  guid = "g0b9LTgMx_O28ojM9WvayOV8OmU"
}