// Add STATUS _TTOKENIZACAO record
query status_ttokenizacao verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "STATUS _TTOKENIZACAO"
    }
  }

  stack {
    db.add "STATUS _TTOKENIZACAO" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_ttokenizacao
  }

  response = $status_ttokenizacao
  guid = "TVLqfFWdKRp6xiFNNuPmyZw_bUE"
}