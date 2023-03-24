from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile, DbtCoreOperation

import os
from dotenv import load_dotenv

load_dotenv()

# This is an alternative to creating GCP blocks in the UI
# (1) insert your own GCS bucket name
# (2) insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!

your_GCS_bucket_name = "magic-the-gathering-381611_mtg_data_lake"  # (1) insert your GCS bucket name
gcs_credentials_block_name = "magic-the-gathering"

service_account_info = {
  "type": "service_account",
  "project_id": os.getenv('GCP_PROJECT_ID'),
  "private_key_id": os.getenv('GCP_PRIVATE_KEY_ID'),
  "private_key": os.getenv('GCP_PRIVATE_KEY'),
  "client_email": os.getenv('GCP_CLIENT_EMAIL'),
  "client_id": os.getenv('GCP_CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/SERVICE_ACCOUNT_EMAIL"
}

credentials_block = GcpCredentials(
    service_account_info=service_account_info
)

credentials_block.save(f"{gcs_credentials_block_name}", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(f"{gcs_credentials_block_name}"),
    bucket=f"{your_GCS_bucket_name}",
)

bucket_block.save(f"{gcs_credentials_block_name}-bucket", overwrite=True)


credentials = GcpCredentials.load(gcs_credentials_block_name)
target_configs = BigQueryTargetConfigs(
    schema="mtg_card_data_dbt",
    credentials=credentials,
)
target_configs.save("mtg-dbt-target-config", overwrite=True)

dbt_cli_profile = DbtCliProfile(
    name="mtg-dbt-cli-profile",
    target="dev",
    target_configs=target_configs,
)
dbt_cli_profile.save("mtg-dbt-cli-profile", overwrite=True)
