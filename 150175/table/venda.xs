table VENDA {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int veiculo_id {
      table = "VEICULO"
    }
  
    int cliente_id {
      table = "CLIENTE"
    }
  
    int vendedor_id {
      table = "FUNCIONARIO"
    }
  
    timestamp data?=now
    decimal valor
    enum tipo_pagamento {
      values = ["venda", "financiamento"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
  guid = "kOui848VbGvY8lr2A_dX7HHvwgY"
}
