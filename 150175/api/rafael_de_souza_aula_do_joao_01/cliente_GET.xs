// Query all CLIENTE records
query cliente verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query CLIENTE {
      return = {type: "list"}
    } as $cliente
  }

  response = $cliente
  guid = "z-PrvWrLziv6YN_gBiRuKjPhKks"
}