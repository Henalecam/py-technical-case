# Processador de Dados de Vendas

Programa Python para processar e analisar dados de clientes e pedidos, gerando relatórios e estatísticas.

## Requisitos

- Python 3.x

## Estrutura de Arquivos

- `clientes.json` - Arquivo com dados dos clientes
- `pedidos.json` - Arquivo com dados dos pedidos
- `processar_dados.py` - Script principal de processamento
- `relatorio.json` - Relatório gerado (criado após execução)

## Como Executar

```bash
python3 processar_dados.py
```

## Lógica do Programa (processar_dados.py)

### Todos os tratamentos de erro foram testados individualmente, buscando cobrir todos os casos possíveis para garantir que o programa funcione corretamente.


### Função main
O core que chama as outras funções, né.
Tratamento para erros de arquivos não encontrados, JSON inválido e arquivo não conter um array JSON e outros erros.

### Função load_json
Leitura dos arquivos JSON.
Passa o parâmetro filename para o arquivo a ser carregado e retorna o conteúdo do arquivo em formato de lista.
Tratamento de erro para arquivo não encontrado, JSON inválido e arquivo não conter um array JSON.

### Função validate_required_fields & validate_numeric_value
Funções para validar se os campos obrigatórios estão presentes no item e se o valor é numérico.
Passamos o item, os campos obrigatórios e o tipo de item para a função.
Se algum campo obrigatório não estiver presente, a função lança um erro.
Se o valor não for numérico, a função lança outro erro.

### Função merge_data
Onde é feita a mesclagem dos dados dos clientes e pedidos.
Verifica se a lista de clientes está vazia, se a lista de pedidos está vazia e se o cliente existe.
Se o cliente não existir, o pedido é ignorado.
Se o cliente existir, o pedido é mesclado com o cliente.
Retorna a lista de pedidos mesclados com os dados dos clientes.

### Função generate_report
Gera o relatório com as estatísticas.
Verifica se a lista de pedidos está vazia.
Calcula o total de pedidos por cliente, o total de receita por país, o melhor produto vendido e o cliente que mais gastou.
Retorna o relatório com as estatísticas em formato de dicionário.

### Função save_report
Salva o relatório em um arquivo Json, se tiver os dados necessários.
Caso contrário terá mensagem de erro de dados vazios ou qualquer outro erro.
