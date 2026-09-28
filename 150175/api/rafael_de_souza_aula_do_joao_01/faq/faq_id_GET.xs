// Get FAQ record
query "faq/{faq_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int faq_id? filters=min:1
  }

  stack {
    db.get FAQ {
      field_name = "id"
      field_value = $input.faq_id
    } as $faq
  
    precondition ($faq != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $faq
  guid = "-I9Hd48rqiAPV7CB0_5qROx_MjA"
}