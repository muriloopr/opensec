// Delete STATUS_OE record.
query "status_oe/{status_oe_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_oe_id? filters=min:1
  }

  stack {
    db.del STATUS_OE {
      field_name = "id"
      field_value = $input.status_oe_id
    }
  }

  response = null
  guid = "eBBX_Se3l3-rddM39pHdmnGA2GY"
}