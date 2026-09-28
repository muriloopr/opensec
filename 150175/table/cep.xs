table CEP {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    timestamp? CREATED_ID?
    text CEP? filters=trim
    text UF? filters=trim
    text CIDADE? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "6m4qOl4-9Elo4c-d-7spDHJ1JZo"
}