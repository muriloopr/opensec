// Query all FAQ records
query faq verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query FAQ {
      return = {type: "list"}
    } as $faq
  }

  response = $faq
  guid = "phrkNhUiY9rfTRcAngh1RV2qzco"
}