// Add TTOKENTIZACAO record
query ttokentizacao verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "TTOKENTIZACAO"
    }
  }

  stack {
    db.add TTOKENTIZACAO {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $ttokentizacao
  }

  response = $ttokentizacao
  guid = "_nKQqGY_VVcoq0jRTav_q435BKQ"
}