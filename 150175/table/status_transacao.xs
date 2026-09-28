table "STATUS_TRANSAÇÃO" {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text stataus_? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "M7q1ZnUVQ2Bl4VliekuLFgYfoiQ"
}