// Query all STATUS_OP records
query status_op verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query STATUS_OP {
      return = {type: "list"}
    } as $status_op
  }

  response = $status_op
  guid = "rRlhjufzyOo6RAokT7RjSTxTsBw"
}