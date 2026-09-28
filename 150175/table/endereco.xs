table "ENDEREÇO" {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int cliente_id? {
      table = "CLIENTE"
    }
  
    text LOGADOR_? filters=trim
    text NUMERO? filters=trim
    text COMPLEMENTO? filters=trim
    text BAIRRO? filters=trim
    text REFERENCIA? filters=trim
    bool PADRAO?
    int cep_id? {
      table = "CEP"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "RAxnedKx2Bv36ZiJpJ7uEOXZz3Y"
}