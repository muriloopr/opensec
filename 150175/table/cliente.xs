table CLIENTE {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id?
    text celular? filters=trim
    text cpf? filters=trim
    int status_clientes_id? {
      table = "STATUS_CLIENTES"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "9bcIWHQEOvrkMZERkFykIkjNzRs"
}