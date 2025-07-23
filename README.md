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
│ └── deploy_dataform.yaml
├── topics_gcp
│ └── pipeline_config.yaml
├── generate_pipeline
│ └── generate_dataform_project.py
├── cloudbuild.yaml
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
schedule: 0 0 * * *
tables:
    - name: sales_summary
        type: table
        schema: analytics
        query: |
            SELECT region, SUM(sales) AS total_sales
            FROM raw.sales
            GROUP BY region

    - name: regional_stats
        type: table
        schema: analytics
        depends_on:
            - sales_summary
        query: |
            SELECT region, total_sales
            FROM {{ ref('sales_summary') }}
            WHERE total_sales > 1000
```

Utilize este exemplo como referência para preencher os campos do seu pipeline.

Preencha cada campo conforme descrito abaixo:

- **project_name**:  
  Nome do projeto Dataform. Utilize um nome descritivo e único para identificar o pipeline.

- **default_schema**:  
  Schema padrão onde as tabelas serão criadas, caso não seja especificado individualmente em cada tabela.

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
     Query SQL responsável pela criação da tabela. Utilize `{{ ref('nome_da_tabela') }}` para referenciar outras tabelas do pipeline.

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

