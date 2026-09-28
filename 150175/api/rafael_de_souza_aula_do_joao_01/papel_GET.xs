// Query all PAPEL records
query papel verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query PAPEL {
      return = {type: "list"}
    } as $papel
  }

  response = $papel
  guid = "80LXQY4DnkRSNm4WQjDNJSL9epU"
}