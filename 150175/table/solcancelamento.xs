table SOLCANCELAMENTO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text motivo? filters=trim
    int Pedido_ID?
    int Status_Solcancelamento_ID?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "LweNUQ6m_tdjtxvrdZlixRDR7y8"
}