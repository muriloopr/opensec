// Delete TTOKENTIZACAO record.
query "ttokentizacao/{ttokentizacao_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int ttokentizacao_id? filters=min:1
  }

  stack {
    db.del TTOKENTIZACAO {
      field_name = "id"
      field_value = $input.ttokentizacao_id
    }
  }

  response = null
  guid = "mfCI4RONxVQ_QrUYYdm1xs1BXPk"
}