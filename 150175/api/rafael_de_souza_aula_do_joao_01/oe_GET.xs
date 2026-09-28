// Query all OE records
query oe verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query OE {
      return = {type: "list"}
    } as $oe
  }

  response = $oe
  guid = "Q3XCRvz4leLv0T-vOP4wczId17Q"
}