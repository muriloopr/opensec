table FUNCIONARIO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text nome filters=trim
    enum cargo {
      values = ["vendedor", "mecanico", "gerente"]
    }
  
    int loja_id {
      table = "LOJA"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
  guid = "9S9pFtv0FS29sTOKEQqUqOaqkdo"
}
