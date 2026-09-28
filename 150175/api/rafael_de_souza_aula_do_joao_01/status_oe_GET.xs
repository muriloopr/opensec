// Query all STATUS_OE records
query status_oe verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query STATUS_OE {
      return = {type: "list"}
    } as $status_oe
  }

  response = $status_oe
  guid = "lzAG8YUbWPr6EXuc2c2k6wQu73E"
}