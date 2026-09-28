// Delete OE record.
query "oe/{oe_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int oe_id? filters=min:1
  }

  stack {
    db.del OE {
      field_name = "id"
      field_value = $input.oe_id
    }
  }

  response = null
  guid = "E5xMqOsHTtNOUEu5pNrlq5NoR1g"
}