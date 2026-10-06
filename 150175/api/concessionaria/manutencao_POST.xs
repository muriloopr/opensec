// Registrar uma nova manutenção para um veículo
query manutencao verb=POST {
  api_group = "CONCESSIONARIA"

  input {
    dblink {
      table = "MANUTENCAO"
    }
  }

  stack {
    // 1. Verificar se o veículo existe
    db.get VEICULO {
      field_name = "id"
      field_value = $input.veiculo_id
    } as $veiculo
  
    precondition ($veiculo != null) {
      error_type = "notfound"
      error = "Veículo não encontrado."
    }
  
    // 2. Adicionar o registro da manutenção
    db.add MANUTENCAO {
      enforce_hidden_fields = false
      data = {
        veiculo_id: $input.veiculo_id,
        mecanico_id: $input.mecanico_id,
        data_inicio: $input.data_inicio,
        descricao: $input.descricao,
        custo: $input.custo,
        created_at: "now"
      }
    } as $manutencao
  
    // 3. Atualizar o status do veículo para 'em_manutencao'
    db.edit VEICULO {
      field_name = "id"
      field_value = $input.veiculo_id
      data = {status: "em_manutencao"}
    }
  }

  response = $manutencao
}
