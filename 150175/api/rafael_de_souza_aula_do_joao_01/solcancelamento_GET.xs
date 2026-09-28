// Query all SOLCANCELAMENTO records
query solcancelamento verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query SOLCANCELAMENTO {
      return = {type: "list"}
    } as $solcancelamento
  }

  response = $solcancelamento
  guid = "0VHZNPIl_nAgead_KXUbZNZ-XIk"
}