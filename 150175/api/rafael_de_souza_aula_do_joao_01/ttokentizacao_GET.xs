// Query all TTOKENTIZACAO records
query ttokentizacao verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query TTOKENTIZACAO {
      return = {type: "list"}
    } as $ttokentizacao
  }

  response = $ttokentizacao
  guid = "UsttcbNy7LefO-3uvb4NzsxkeFw"
}