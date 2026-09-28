// Query all CEP records
query cep verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query CEP {
      return = {type: "list"}
    } as $cep
  }

  response = $cep
  guid = "DKmILhtO0HMkAaxtZiOWoQ-Obsg"
}