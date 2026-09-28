// Add FAQ record
query faq verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "FAQ"
    }
  }

  stack {
    db.add FAQ {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $faq
  }

  response = $faq
  guid = "ZLhQNsf-tyEOg4k4f_1wbKYoesM"
}