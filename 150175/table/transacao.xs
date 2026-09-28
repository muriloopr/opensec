table "TRANSAÇÃO" {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text clienteas? filters=trim
    text idpayment? filters=trim
    text tipo? filters=trim
    decimal valor?
    text datavenc? filters=trim
    text descricao? filters=trim
    int status_transa_o_id? {
      table = "STATUS_TRANSAÇÃO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "O4_aqBzspR1Tr3x_bVO8g_jZ_Rc"
}