// STATUS DO CLIENTE GERAL
table STATUS_CLIENTES {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text status? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  tags = ["módulo_01"]
  guid = "69LBDoz_zhIIU0RGo6wCy1nB-dI"
}