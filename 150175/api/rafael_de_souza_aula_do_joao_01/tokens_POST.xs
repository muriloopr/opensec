// Add TOKENS record
query tokens verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "TOKENS"
    }
  }

  stack {
    db.add TOKENS {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $tokens
  }

  response = $tokens
  guid = "ZzGTdsSX4woxAqoHYYBlRYE9nkw"
}