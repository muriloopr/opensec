// Query all TRANSAÇÃO records
query transa_o verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query "TRANSAÇÃO" {
      return = {type: "list"}
    } as $transa_o
  }

  response = $transa_o
  guid = "UNEs6yNa17Eh7rn1rYeE4PQ4LRM"
}