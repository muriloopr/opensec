table MANUTENCAO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int veiculo_id {
      table = "VEICULO"
    }
  
    int mecanico_id {
      table = "FUNCIONARIO"
    }
  
    timestamp data_inicio?=now
    timestamp? data_fim
    text descricao filters=trim
    decimal custo
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
}
