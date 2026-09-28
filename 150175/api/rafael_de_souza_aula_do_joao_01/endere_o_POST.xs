// Add ENDEREÇO record
query endere_o verb=POST {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    dblink {
      table = "ENDEREÇO"
    }
  }

  stack {
    db.add "ENDEREÇO" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $endere_o
  }

  response = $endere_o
  guid = "CAy3lMS1IW6ZSQTFXpzpsMviQD4"
}