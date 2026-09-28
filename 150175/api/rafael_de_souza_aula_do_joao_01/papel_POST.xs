// Add PAPEL record
query papel verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "PAPEL"
    }
  }

  stack {
    db.add PAPEL {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $papel
  }

  response = $papel
  guid = "x0_MWB-zJHIVO3ymJmF5-px6TDc"
}