cadastro =(input('digite seu email:')) 
senha = input('digite sua senha:')
nome = input('digite seu nome:')
print('cadastro realizado com sucesso!!')
while not cadastro or not senha or not nome:
    print ('cadastro com falta de dados,  repita o processo')
    break