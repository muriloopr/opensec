table VEICULO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text marca filters=trim
    text modelo filters=trim
    int ano
    decimal preco
    enum status {
      values = ["disponivel", "vendido", "em_manutencao"]
    }
  
    int loja_id {
      table = "LOJA"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
  guid = "HhmXzZ62d3VATTy5r4STIGHSXuQ"
}
