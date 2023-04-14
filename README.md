# CLSiM
# Centro Logístico de Simulação Meteorológica

O CLSiM é o front-end para execução de jobs WRF.  Nele podem ser
selecionados diversos parâmetros como a região, data e hora iniciais e o
intervalo de simulação para execução do modelo.  Os resultados da simulação
são armazenados e disponibilizados por um período de duas semanas para
download, ao fim do qual são removidos para liberação de espaço.

Foi desenvolvido em linguagem Python, utilizando a biblioteca StreamLit para
criação da interface.  Os jobs solicitados são enviados via message queue
para um pool de servidores.  O primeiro servidor disponível bloqueia a
mensagem na fila e executa a simulação.  Ao término remove a mensagem da
fila, armazena o resultado e envia um e-mail de aviso ao solicitante.  Caso
haja algum problema durante a execução, a mensagem é desbloqueada e o
próximo servidor disponível assume a execução.
 