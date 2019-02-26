import sqlalchemy
from sqlalchemy.dialects import postgresql

from goobox_nodes_api.resources import database_metadata

__all__ = ["sia_node"]


sia_node = sqlalchemy.Table(
    "sia_node",
    database_metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("accepting_contracts", sqlalchemy.Boolean),
    sqlalchemy.Column("max_download_batch_size", sqlalchemy.Integer),
    sqlalchemy.Column("max_duration", sqlalchemy.Integer),
    sqlalchemy.Column("max_revise_batch_size", sqlalchemy.Integer),
    sqlalchemy.Column("net_address", sqlalchemy.String),
    sqlalchemy.Column("remaining_storage", sqlalchemy.Integer),
    sqlalchemy.Column("sector_size", sqlalchemy.Integer),
    sqlalchemy.Column("total_storage", sqlalchemy.Integer),
    sqlalchemy.Column("unlock_hash", sqlalchemy.String),
    sqlalchemy.Column("window_size", sqlalchemy.Integer),
    sqlalchemy.Column("collateral", sqlalchemy.String),
    sqlalchemy.Column("max_collateral", sqlalchemy.String),
    sqlalchemy.Column("contract_price", sqlalchemy.String),
    sqlalchemy.Column("download_bandwidth_price", sqlalchemy.String),
    sqlalchemy.Column("storage_price", sqlalchemy.String),
    sqlalchemy.Column("upload_bandwidth_price", sqlalchemy.String),
    sqlalchemy.Column("revision_number", sqlalchemy.Integer),
    sqlalchemy.Column("version", sqlalchemy.String),
    sqlalchemy.Column("first_seen", sqlalchemy.Integer),
    sqlalchemy.Column("historic_downtime", sqlalchemy.Integer),
    sqlalchemy.Column("historic_uptime", sqlalchemy.Integer),
    sqlalchemy.Column("historic_failed_interactions", sqlalchemy.Integer),
    sqlalchemy.Column("historic_successful_interactions", sqlalchemy.Integer),
    sqlalchemy.Column("recent_failed_interactions", sqlalchemy.Integer),
    sqlalchemy.Column("recent_successful_interactions", sqlalchemy.Integer),
    sqlalchemy.Column("last_historic_update", sqlalchemy.Integer),
    sqlalchemy.Column("public_key_string", sqlalchemy.String),
    sqlalchemy.Column("ipnets", postgresql.ARRAY(postgresql.INET)),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("country", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.String),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
)
