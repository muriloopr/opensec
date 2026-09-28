// Delete FAQ record.
query "faq/{faq_id}" verb=DELETE {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int faq_id? filters=min:1
  }

  stack {
    db.del FAQ {
      field_name = "id"
      field_value = $input.faq_id
    }
  }

  response = null
  guid = "QAMw6KaAAzQuMyW3q5sbuVQiPlE"
}