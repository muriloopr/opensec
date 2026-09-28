// Edit STATUS_OE record
query "status_oe/{status_oe_id}" verb=PATCH {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_oe_id? filters=min:1
    dblink {
      table = "STATUS_OE"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch STATUS_OE {
      field_name = "id"
      field_value = $input.status_oe_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $status_oe
  }

  response = $status_oe
  guid = "77qnvBzeJkxjsB3aLDnJ6XyUilk"
}