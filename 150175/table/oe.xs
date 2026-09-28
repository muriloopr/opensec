table OE {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int pedido_id? {
      table = "PEDIDO"
    }
  
    int status_oe_id? {
      table = "STATUS_OE"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "y0PduTI6N0PNIz3NKIMulaVOa_4"
}