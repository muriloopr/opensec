// Query all TOKENS records
query tokens verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query TOKENS {
      return = {type: "list"}
    } as $tokens
  }

  response = $tokens
  guid = "mLrgUe-CkhKQqoKwpb9b_Mc0mbw"
}