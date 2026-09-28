// Delete STATUS_OP record.
query "status_op/{status_op_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int status_op_id? filters=min:1
  }

  stack {
    db.del STATUS_OP {
      field_name = "id"
      field_value = $input.status_op_id
    }
  }

  response = null
  guid = "BT_WO3vs3b57UCistx23eAVxZ2I"
}