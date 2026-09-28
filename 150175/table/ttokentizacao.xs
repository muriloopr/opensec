table TTOKENTIZACAO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int cliente_id? {
      table = "CLIENTE"
    }
  
    text det_cartao_encript? filters=trim
    int status_ttokenizacao_id? {
      table = "STATUS _TTOKENIZACAO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "XkYTZQG2EXzDDUQ052rPH4W0vZM"
}