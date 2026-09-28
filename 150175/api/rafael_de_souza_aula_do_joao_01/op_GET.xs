// Query all OP records
query op verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
  }

  stack {
    db.query OP {
      return = {type: "list"}
    } as $op
  }

  response = $op
  guid = "tKS0DOp3QpBsqseevy6xt13YTNc"
}