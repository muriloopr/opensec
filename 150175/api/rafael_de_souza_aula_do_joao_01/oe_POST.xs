// Add OE record
query oe verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "OE"
    }
  }

  stack {
    db.add OE {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $oe
  }

  response = $oe
  guid = "SOfEDDN_DlFlkEBni_U392benmE"
}