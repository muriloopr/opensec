// Obter detalhes de um veículo específico
query "veiculo/{veiculo_id}" verb=GET {
  api_group = "CONCESSIONARIA"

  input {
    int veiculo_id
  }

  stack {
    db.get VEICULO {
      field_name = "id"
      field_value = $input.veiculo_id
    } as $veiculo
  
    precondition ($veiculo != null) {
      error_type = "notfound"
      error = "Veículo não encontrado."
    }
  }

  response = $veiculo
}
