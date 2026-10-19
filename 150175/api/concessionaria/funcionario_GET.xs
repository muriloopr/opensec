// Listar todos os funcionários
query funcionario verb=GET {
  api_group = "CONCESSIONARIA"

  input {
    int loja_id?
  }

  stack {
    db.query FUNCIONARIO {
      where = $db.FUNCIONARIO.loja_id ==? $input.loja_id
      return = {type: "list"}
    } as $funcionarios
  }

  response = $funcionarios
  guid = "FIm6sGVdIvepQ2ThUPonBEmVuB4"
}
