# Fluxo de integração entre ERP e CRM

Este projeto tem como objetivo integrar um ERP com um CRM, utilizando o conceito de Event-Driven Architecture (EDA). O fluxo de integração é composto por dois lambdas, um que recebe os dados do ERP e os converte em um formato padronizado, e outro que lê os dados do S3 e os integra com o CRM. Os dados são armazenados no S3 para garantir a persistência e a escalabilidade do sistema.

## Arquitetura

- **Lambda 1**: recebe os dados do ERP e converte-os em um formato padronizado.
- **S3**: armazena os dados gerados pelo primeiro lambda.
- **Lambda 2**: lê os dados do S3 e os integra com o CRM.

## Como rodar o projeto

### Pré-requisitos

- Node.js
- Serverless Framework

### Usuário AWS

Para rodar o projeto, é necessário ter um usuário na AWS com as seguintes permissões:

- AmazonAPIGatewayAdministrator
- AmazonAPIGatewayInvokeFullAccess
- AmazonS3FullAccess
- AWSCloudFormationFullAccess
- AWSLambda_FullAccess
- CloudWatchFullAccess
- IAMFullAccess

Após a criação do usuário, é necessário criar uma chave de acesso e armazená-las para execução do deploy (Chave de acesso = S3_ACCESS_KEY e Chave secreta de acesso = S3_SECRET_KEY).

### Configuração

1. Clone o repositório
2. Instale o `serverless` globalmente

```bash
npm install -g serverless
```

3. Configure o serverless framework

O Serverless Framework necessita de uma conta criada, para isso é necessário realizar o login com o comando `serverless login` e selecionar a opção de `Login/Register` e criar um app nomeado `crm-data`.

Após a instalação das dependências e a configuração do usuário AWS, é necessário configurar o arquivo `serverless.yml` com as credenciais da AWS.

```yaml
# Colocando aqui o nome de sua organização e mantendo o restante após isso
org: awscrm
```

4. Credenciais AWS

O projeto foi configurado para utilizar as credenciais da AWS através de variáveis de ambiente. Para isso, é necessário exportar as variáveis de ambiente `S3_ACCESS_KEY` e `S3_SECRET_KEY` com as credenciais da AWS.

```bash
export S3_ACCESS_KEY=<CHAVE_DE_ACESSO>
export S3_SECRET_KEY=<CHAVE_SECRETA_DE_ACESSO>
```

Para windows, é necessário utilizar o comando `set` ao invés de `export`. Caso não funcione bastar adicionar as variáveis de ambiente no arquivo `serverless.yml` no environment dos lambdas.

```yaml
environment:
  S3_ACCESS_KEY: <CHAVE_DE_ACESSO>
  S3_SECRET_ACCESS_KEY: <CHAVE_DE_ACESSO_SECRETA>
```

### Deploy

Para fazer o deploy do ambiente, já com as credenciais configuradas, basta rodar o comando:

```bash
serverless deploy
```

Após o deploy, você deve ver uma saída semelhante a esta:

```
Deploying "crm-data" to stage "dev" (us-east-1)

✔ Service deployed to stack crm-data-dev (90s)

endpoint: POST - <URL_DO_LAMBDA_PARA_REQUEST>
functions:
  data_process: crm-data-dev-data_process (5.7 kB)
  read_data: crm-data-dev-read_data (5.7 kB)
```

### Execução

Após o deploy, você pode fazer uma requisição POST para o endpoint do Lambda `data_process` com o seguinte payload:

```json
[
  {
    "id": 10001,
    "valor": 152.0,
    "data": "10/01/2024",
    "frete": 5.9,
    "desconto": "5%",
    "status": "finished"
  },
  {
    "id": 10002,
    "valor": 250.0,
    "data": "10/01/2024",
    "frete": 5.9,
    "desconto": "R$50,00",
    "status": "finished"
  }
]
```

Também pode ser usado o JSON contido no arquivo `erp_data.json` para fazer a requisição, localizado na pasta `files`.

Uma resposta semelhante a esta deve ser retornada:

```json
{
  "statusCode": 200,
  "body": {
    "message": "ERP data processed successfully",
    "imported_data": [
      {
        "id": 10001,
        "valor": 152.0,
        "data": "2024-01-10",
        "frete": 5.9,
        "desconto": 7.6,
        "status": "concluido"
      },
      {
        "id": 10002,
        "valor": 250.0,
        "data": "2024-01-10",
        "frete": 5.9,
        "desconto": 50.0,
        "status": "concluido"
      }
    ]
  }
}
```

É possível verificar os arquivos gerados no S3, e verificar se os dados foram armazenados corretamente. Assim como acompanhar o log do lambda no CloudWatch.

O segundo lambda, `read_data`, irá ler os dados do S3 e integrá-los com o CRM. Ele será executado automaticamente após o primeiro lambda ser executado. Portando não é necessário fazer uma requisição para ele, basta aguardar a execução, e acessar o CloudWatch para verificar o log.

## Referências

- [Serverless Framework](https://www.serverless.com/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Event-Driven Architecture](https://aws.amazon.com/event-driven-architecture/)
