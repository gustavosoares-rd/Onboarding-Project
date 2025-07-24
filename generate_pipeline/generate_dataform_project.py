import os
import yaml
import uuid
import shutil
from pathlib import Path
from google.cloud import dataform_v1beta1 as dataform

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "topics_gcp" / "pipeline_config.yaml"
SQL_PATH = BASE_DIR / "topics_gcp" / "sql"
TEMP_WORKSPACE = BASE_DIR / "temp_workspace"

GCP_REGION = "us-central1"

def load_config():
    """
    Loads the pipeline configuration from a YAML file.

    This function reads the YAML file located at CONFIG_PATH and parses its contents
    into a Python dictionary using PyYAML.

    Returns:
        dict: The parsed configuration containing project settings such as:
              - project_name (str)
              - bigquery_project (str)
              - default_schema (str)
              - schedule (str)
              - tables (list)
    """


    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def create_sqlx_files(config):
    """
    Generates .sqlx files from a pipeline configuration for deployment to Dataform.

    This function performs the following:
    - Creates a temporary 'definitions' directory inside TEMP_WORKSPACE.
    - Iterates through the list of tables defined in the pipeline configuration.
    - For each table:
        - Builds a dictionary containing the table's type, name, schema,
          optional dependencies, and the SQL query loaded from a referenced .sql file.
        - Saves the dictionary as a .sqlx file in the 'definitions' directory using YAML format.

    These generated .sqlx files are later used to deploy the pipeline to Dataform via the API.

    Parameters:
        config (dict): A dictionary containing the pipeline configuration, including:
            - project_name (str): Logical name of the project (used as the Dataform repository ID).
            - default_schema (str): Default BigQuery schema for the tables.
            - tables (list): List of tables to be created, where each table is a dict with:
                - name (str): Table name.
                - type (str): Table type (e.g., "table", "view").
                - schema (str, optional): Schema override (defaults to `default_schema`).
                - query (str): Name of the .sql file containing the table's SQL logic.
                - depends_on (list, optional): List of dependent table names.
    """


    tables = config["tables"]
    project = config["project_name"]
    default_schema = config["default_schema"]

    workspace_dir = TEMP_WORKSPACE / "definitions"
    workspace_dir.mkdir(parents=True, exist_ok=True)

    for table in tables:
        content = {
            "type": table["type"],
            "name": table["name"],
            "schema": table.get("schema", default_schema),
        }

        if "depends_on" in table:
            content["dependencies"] = table["depends_on"]

        sql_file = SQL_PATH / table["query"]
        with open(sql_file, "r") as f:
            content["query"] = f.read()

        sqlx_file = workspace_dir / f"{table['name']}.sqlx"
        with open(sqlx_file, "w") as f:
            yaml.dump(content, f)

def deploy_to_dataform(config):
     """
    Deploys the generated Dataform SQLX files to a Dataform repository and configures the pipeline schedule.

    This function performs the following steps:
    - Initializes a Dataform client.
    - Uses the 'bigquery_project' and 'project_name' from the config to identify the target Dataform repository.
    - Creates a new workspace within the repository for this deployment.
    - Reads all .sqlx files from the temporary definitions directory.
    - Uploads these files to the workspace in Dataform.
    - Commits the changes in the workspace to the repository.
    - Creates a release configuration with a cron schedule for automated pipeline runs.

    Parameters:
        config (dict): A dictionary containing pipeline configuration with keys:
            - bigquery_project (str): The GCP project ID where the Dataform repository exists.
            - project_name (str): The name of the Dataform repository to deploy to.
            - schedule (str): A cron expression defining the pipeline's run schedule.

    Prints:
        Logs indicating progress at each key step of deployment.
    """


    client = dataform.DataformClient()
    bigquery_project = config["bigquery_project"]
    repo_id = config["project_name"]

    parent = f"projects/{bigquery_project}/locations/{GCP_REGION}/repositories/{repo_id}"
    workspace_id = f"workspace-{uuid.uuid4().hex[:6]}"
    workspace_path = client.workspace_path(bigquery_project, GCP_REGION, repo_id, workspace_id)

    client.create_workspace(parent=parent, workspace_id=workspace_id, workspace={})
    print(f"Workspace criado: {workspace_id} em {bigquery_project}")

    definitions_path = TEMP_WORKSPACE / "definitions"
    entries = {}
    for file_path in definitions_path.glob("*.sqlx"):
        with open(file_path, "r") as f:
            content = f.read()
        entries[f"definitions/{file_path.name}"] = content

    client.write_file_tree(workspace=workspace_path, file_tree={"files": entries})
    print(f"Arquivos enviados para workspace {workspace_id}")

    commit_request = dataform.CommitWorkspaceChangesRequest(
        name=workspace_path,
        author={"name": "Data Engineer", "email": "data@company.com"},
        commit_message="Deploy automático via script",
    )
    client.commit_workspace_changes(request=commit_request)
    print(f"Commit realizado")


    release_config_id = f"release-{uuid.uuid4().hex[:6]}"
    release_config = dataform.ReleaseConfig(
        name=f"{parent}/releaseConfigs/{release_config_id}",
        git_commitish="HEAD",
        included_tags=[],
        included_paths=["definitions/"],
        cron_schedule=config["schedule"]
    )
    client.create_release_config(
        parent=parent,
        release_config_id=release_config_id,
        release_config=release_config
    )
    print(f"Schedule configurado: {config['schedule']}")

def clean_workspace():
    """
    Deletes the temporary workspace directory used to store generated files.

    This function checks if the TEMP_WORKSPACE directory exists and removes it entirely,
    cleaning up any temporary files created during the pipeline generation process.
    """

    
    if TEMP_WORKSPACE.exists():
        shutil.rmtree(TEMP_WORKSPACE)

if __name__ == "__main__":
    config = load_config()
    clean_workspace()
    create_sqlx_files(config)
    deploy_to_dataform(config)
    clean_workspace()
