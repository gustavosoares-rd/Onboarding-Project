# Onboarding-Project
## Sumário

- [Estrutura](#estrutura)
- [Configuração do Pipeline](#configuração-do-pipeline)
- [Estrutura do Arquivo YAML](#estrutura-do-arquivo-yaml)
- [Deploy](#deploy)



## Estrutura
 ```sh
├── .github/
│ └── workflows/
│   └── deploy_dataform.yaml
├── topics_gcp
│ └── sql_files/
│   └── arquivo.sql
│ └── pipeline_config.yaml
├── generate_pipeline
│ └── generate_dataform_project.py
├── requirements.txt
└── README.md
```

## Configuração do Pipeline

### Documentação para Configuração do Pipeline Dataform

Este arquivo YAML serve como guia para a criação de pipelines no Dataform. Siga os passos abaixo para garantir o correto preenchimento e funcionamento do pipeline:

### Passos Iniciais

1. **Clonar o Repositório**
    - Faça o clone do repositório para sua máquina local utilizando o comando:
      ```
      git clone https://github.com/gustavosoares-rd/Onboarding-Project.git
      ```
    - Navegue até o diretório do projeto clonado.

2. **Criar uma Nova Branch**
    - Crie uma branch para suas alterações:
      ```
      git switch -c nome-da-sua-branch
      ```

## Estrutura do Arquivo YAML

Abaixo segue um exemplo de como preencher o arquivo YAML para configuração do pipeline Dataform:

```yaml
project_name: my_dataform_project
default_schema: analytics
bigquery_project: rd-isdpoctmp-stg-01
schedule: 0 0 * * *
tables:
  - name: sales_summary
    type: table
    schema: analytics
    query: sales_summary.sql
    columns:
      - name: sale_id
        type: STRING
        description: Unique identifier for the sale
      - name: amount
        type: FLOAT
        description: Total amount of the sale
      - name: sale_date
        type: DATE
        description: Date the sale was made

  - name: regional_stats
    type: table
    schema: analytics
    depends_on:
      - sales_summary
    query: regional_stats.sql
    columns:
      - name: region
        type: STRING
        description: Sales region
      - name: total_sales
        type: FLOAT
        description: Total sales for the region
      - name: report_date
        type: DATE
        description: Date of the report
```

Utilize este exemplo como referência para preencher os campos do seu pipeline.

Preencha cada campo conforme descrito abaixo:

- **project_name**:  
  Nome do projeto Dataform. Utilize um nome descritivo e único para identificar o pipeline.

- **default_schema**:  
  Schema padrão onde as tabelas serão criadas, caso não seja especificado individualmente em cada tabela.

- **bigquery_project**:  
  Nome do seu projeto do BigQuery, onde o projeto dataform sera criado

- **schedule**:
  O parâmetro schedule especifica o agendamento de execução automática de uma tarefa, geralmente usando uma expressão de tempo (como cron).

- **tables**:  
  Lista de tabelas que serão criadas no pipeline. Para cada tabela, preencha os seguintes campos:

  - **name**:  
     Nome da tabela que será criada no Dataform.

  - **type**:  
     Tipo do objeto a ser criado. Exemplo: `table` para tabelas físicas.

  - **schema**:  
     Schema onde a tabela será criada. Caso não seja informado, será utilizado o `default_schema`.

  - **depends_on** (opcional):  
     Lista de tabelas das quais esta tabela depende. Utilize quando a tabela atual utiliza dados de outras tabelas criadas no pipeline.

  - **query**:  
     Dentro da pasta topics_gcp/sql_files, crie um novo arquivo .sql com sua query e passe o nome desse aquivo no parametro do yaml.
     A Query SQL é responsável pela criação da tabela. Utilize `{{ ref('nome_da_tabela') }}` para referenciar outras tabelas do pipeline.
  
  - **columns** (opcional):  
     Lista de colunas que compõem a tabela. Cada coluna deve conter:
     
     - `name`: Nome da coluna.  
     - `type`: Tipo de dado da coluna (por exemplo, `STRING`, `INT64`, `DATE`, etc.).  
     - `description`: Breve descrição da finalidade ou conteúdo da coluna.  

     Essa especificação é útil para documentar o esquema da tabela e pode ser usada para geração de documentação automatizada ou validação de esquemas.


## Deploy

1. **Salvar e Validar**
    - Salve o arquivo após preencher todos os campos necessários.
    - Valide a sintaxe YAML para evitar erros de formatação.

2. **Commit e Push**
    - Faça o commit das suas alterações:
      ```
      git add .
      git commit -m "Adiciona novo pipeline Dataform"
      git push origin nome-da-sua-branch
      ```

3. **Abrir Pull Request**
    - Acesse o repositório no GitHub e abra um Pull Request (PR) da sua branch para a branch principal (`main`).
    - Descreva as alterações realizadas e aguarde a revisão.

**Observação:**  
Preencha todos os campos obrigatórios e siga o padrão estabelecido para garantir a integração correta do pipeline ao projeto.

