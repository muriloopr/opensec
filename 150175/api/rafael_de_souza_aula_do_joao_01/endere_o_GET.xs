// Query all ENDEREÇO records
query endere_o verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query "ENDEREÇO" {
      return = {type: "list"}
    } as $endere_o
  }

  response = $endere_o
  guid = "wP0cH0caeB2GZVGWsNataLLoJGI"
}