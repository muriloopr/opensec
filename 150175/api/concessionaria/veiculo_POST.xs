// Adicionar um novo veículo ao estoque
query veiculo verb=POST {
  api_group = "CONCESSIONARIA"

  input {
    dblink {
      table = "VEICULO"
    }
  }

  stack {
    db.add VEICULO {
      enforce_hidden_fields = false
      data = {
        marca: $input.marca,
        modelo: $input.modelo,
        ano: $input.ano,
        preco: $input.preco,
        status: $input.status,
        loja_id: $input.loja_id,
        created_at: "now"
      }
    } as $veiculo
  }

  response = $veiculo
}
