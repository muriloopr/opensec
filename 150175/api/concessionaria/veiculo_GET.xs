// Listar todos os veículos
query veiculo verb=GET {
  api_group = "CONCESSIONARIA"

  input {
    enum status? {
      values = ["disponivel", "vendido", "em_manutencao"]
    }
  }

  stack {
    db.query VEICULO {
      where = $db.VEICULO.status ==? $input.status
      return = {type: "list"}
    } as $veiculos
  }

  response = $veiculos
}
