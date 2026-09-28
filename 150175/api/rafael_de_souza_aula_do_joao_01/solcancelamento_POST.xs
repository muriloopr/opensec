// Add SOLCANCELAMENTO record
query solcancelamento verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "SOLCANCELAMENTO"
    }
  }

  stack {
    db.add SOLCANCELAMENTO {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $solcancelamento
  }

  response = $solcancelamento
  guid = "kphjLj7F-YhR5Cf6obQFih3qsLk"
}