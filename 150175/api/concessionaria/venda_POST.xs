// Registrar uma nova venda e atualizar o status do veículo
query venda verb=POST {
  api_group = "CONCESSIONARIA"

  input {
    dblink {
      table = "VENDA"
    }
  }

  stack {
    // 1. Verificar se o veículo está disponível
    db.get VEICULO {
      field_name = "id"
      field_value = $input.veiculo_id
    } as $veiculo
  
    precondition ($veiculo != null) {
      error_type = "notfound"
      error = "Veículo não encontrado."
    }
  
    precondition ($veiculo.status == "disponivel") {
      error_type = "inputerror"
      error = "Este veículo não está disponível para venda."
    }
  
    // 2. Adicionar o registro da venda
    db.add VENDA {
      enforce_hidden_fields = false
      data = {
        veiculo_id: $input.veiculo_id,
        cliente_id: $input.cliente_id,
        vendedor_id: $input.vendedor_id,
        data: $input.data,
        valor: $input.valor,
        tipo_pagamento: $input.tipo_pagamento
      }
    } as $venda
  
    // 3. Atualizar o status do veículo para 'vendido'
    db.edit VEICULO {
      field_name = "id"
      field_value = $input.veiculo_id
      data = {status: "vendido"}
    }
  }

  response = $venda
}
