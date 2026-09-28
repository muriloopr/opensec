// Get SOLCANCELAMENTO record
query "solcancelamento/{solcancelamento_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int solcancelamento_id? filters=min:1
  }

  stack {
    db.get SOLCANCELAMENTO {
      field_name = "id"
      field_value = $input.solcancelamento_id
    } as $solcancelamento
  
    precondition ($solcancelamento != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $solcancelamento
  guid = "RDfhQ_hnUXQG8BPRSy1YbzMQs1s"
}