import sqlalchemy
from sqlalchemy.dialects import postgresql

from goobox_nodes.resources import database_metadata

__all__ = ["sia_node"]


sia_node = sqlalchemy.Table(
    "sia_node",
    database_metadata,
    sqlalchemy.Column("id", postgresql.UUID, primary_key=True),
    sqlalchemy.Column("accepting_contracts", sqlalchemy.Boolean),
    sqlalchemy.Column("max_download_batch_size", sqlalchemy.BigInteger),
    sqlalchemy.Column("max_duration", sqlalchemy.BigInteger),
    sqlalchemy.Column("max_revise_batch_size", sqlalchemy.BigInteger),
    sqlalchemy.Column("net_address", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("remaining_storage", sqlalchemy.BigInteger),
    sqlalchemy.Column("sector_size", sqlalchemy.BigInteger),
    sqlalchemy.Column("total_storage", sqlalchemy.BigInteger),
    sqlalchemy.Column("unlock_hash", sqlalchemy.String),
    sqlalchemy.Column("window_size", sqlalchemy.BigInteger),
    sqlalchemy.Column("collateral", sqlalchemy.String),
    sqlalchemy.Column("max_collateral", sqlalchemy.String),
    sqlalchemy.Column("contract_price", sqlalchemy.String),
    sqlalchemy.Column("download_bandwidth_price", sqlalchemy.String),
    sqlalchemy.Column("storage_price", sqlalchemy.String),
    sqlalchemy.Column("upload_bandwidth_price", sqlalchemy.String),
    sqlalchemy.Column("revision_number", sqlalchemy.BigInteger),
    sqlalchemy.Column("version", sqlalchemy.String),
    sqlalchemy.Column("first_seen", sqlalchemy.BigInteger),
    sqlalchemy.Column("historic_downtime", sqlalchemy.BigInteger),
    sqlalchemy.Column("historic_uptime", sqlalchemy.BigInteger),
    sqlalchemy.Column("historic_failed_interactions", sqlalchemy.BigInteger),
    sqlalchemy.Column("historic_successful_interactions", sqlalchemy.BigInteger),
    sqlalchemy.Column("recent_failed_interactions", sqlalchemy.BigInteger),
    sqlalchemy.Column("recent_successful_interactions", sqlalchemy.BigInteger),
    sqlalchemy.Column("last_historic_update", sqlalchemy.BigInteger),
    sqlalchemy.Column("public_key_string", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("ipnets", postgresql.ARRAY(postgresql.INET)),
    sqlalchemy.Column("country", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.String),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
)
