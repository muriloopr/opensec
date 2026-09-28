// Get PEDIDO record
query "pedido/{pedido_id}" verb=GET {
  api_group = "RAFAEL DE SOUZA AULA DO JOÃO 01"

  input {
    int pedido_id? filters=min:1
  }

  stack {
    db.get PEDIDO {
      field_name = "id"
      field_value = $input.pedido_id
    } as $pedido
  
    precondition ($pedido != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $pedido
  guid = "PefQj631J7UESZwm8AhRvZf3OKg"
}