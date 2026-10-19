table LOJA {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text nome filters=trim
    text endereco? filters=trim
    text telefone? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
  guid = "zNBnymELa4bZX7pI505d-d75NFw"
}
