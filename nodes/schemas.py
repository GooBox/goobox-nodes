from marshmallow import Schema, validate
from marshmallow.fields import Boolean, UUID, Integer, String, Float, List


class SiaNode(Schema):
    id = UUID(title="id", description="Sia unique identifier.", required=True, dump_only=True)
    accepting_contracts = Boolean(
        title="accepting_contracts", description="True if the host is accepting new contracts."
    )
    max_download_batch_size = Integer(
        title="max_download_batch_size",
        description="Maximum number of bytes that the host will allow to be requested by a single download request",
    )
    max_duration = Integer(
        title="max_duration",
        description="Maximum duration in blocks that a host will allow for a file contract. The host commits to "
                    "keeping files for the full duration under the threat of facing a large penalty for losing or "
                    "dropping data before the duration is complete. The storage proof window of an incoming file "
                    "contract must end before the current height + maxduration.",
    )
    max_revise_batch_size = Integer(
        title="max_revise_batch_size",
        description="Maximum size in bytes of a single batch of file contract revisions. Larger batch sizes allow for "
                    "higher throughput as there is significant communication overhead associated with performing a "
                    "batch upload.",
    )
    net_address = String(
        title="net_address",
        description="Remote address of the host. It can be an IPv4, IPv6, or hostname, along with the port. IPv6 "
                    "addresses are enclosed in square brackets.",
    )
    remaining_storage = Integer(
        title="remaining_storage", description="Unused storage capacity the host claims it has."
    )
    sector_size = Integer(
        title="sector_size",
        description="Smallest amount of data in bytes that can be uploaded or downloaded to or from the host.",
    )
    total_storage = Integer(
        title="total_storage", description="Total amount of storage capacity the host claims it has."
    )
    unlock_hash = String(
        title="unlock_hash", description="Address at which the host can be paid when forming file contracts."
    )
    window_size = Integer(
        title="window_size",
        description="A storage proof window is the number of blocks that the host has to get a storage proof onto the "
                    "blockchain. The window size is the minimum size of window that the host will accept in a file "
                    "contract.",
    )
    collateral = String(
        title="collateral",
        description="The maximum amount of money that the host will put up as collateral for storage that is contracted"
                    " by the renter.",
    )
    max_collateral = String(
        title="max_collateral",
        description="The maximum amount of collateral that the host will put into a single file contract.",
    )
    contract_price = String(
        title="contract_price",
        description="The price that a renter has to pay to create a contract with the host. The payment is intended "
                    "to cover transaction fees for the file contract revision and the storage proof that the host will "
                    "be submitting to the blockchain.",
    )
    download_bandwidth_price = String(
        title="download_bandwidth_price",
        description="The price that a renter has to pay when downloading data from the host.",
    )
    storage_price = String(
        title="storage_price", description="The price that a renter has to pay to store files with the host."
    )
    upload_bandwidth_price = String(
        title="upload_bandwidth_price",
        description="The price that a renter has to pay when uploading data to the host.",
    )
    revision_number = Integer(
        title="revision_number",
        description="The revision number indicates to the renter what iteration of settings the host is currently at. "
                    "Settings are generally signed. If the renter has multiple conflicting copies of settings from "
                    "the host, the renter can expect the one with the higher revision number to be more recent.",
    )
    version = String(title="version", description="The version of the host.")
    first_seen = Integer(
        title="first_seen", description="Firstseen is the last block height at which this host was announced."
    )
    historic_downtime = Integer(
        title="historic_downtime", description="Total amount of time the host has been offline."
    )
    historic_uptime = Integer(title="historic_uptime", description="Total amount of time the host has been online.")
    historic_failed_interactions = Integer(
        title="historic_failed_interactions", description="Number of historic failed interactions with the host."
    )
    historic_successful_interactions = Integer(
        title="historic_successful_interactions",
        description="Number of historic successful interactions with the host.",
    )
    recent_failed_interactions = Integer(
        title="recent_failed_interactions", description="Number of recent failed interactions with the host."
    )
    recent_successful_interactions = Integer(
        title="recent_successful_interactions", description="Number of recent successful interactions with the host."
    )
    last_historic_update = Integer(
        title="last_historic_update",
        description="The last time that the interactions within scanhistory have been compressed into the historic "
                    "ones.",
    )
    public_key_string = String(
        title="public_key_string",
        description="The string representation of the full public key, used when calling /hostdb/hosts.",
    )
    ipnets = List(
        String(),
        title="ipnets",
        description='List of IP subnet masks used by the host. For IPv4 the /24 and for IPv6 the /54 subnet mask is '
                    'used. A host can have either one IPv4 or one IPv6 subnet or one of each. E.g. these lists are '
                    'valid: [ "IPv4" ], [ "IPv6" ] or [ "IPv4", "IPv6" ]. The following lists are invalid: [ "IPv4", '
                    '"IPv4" ], [ "IPv4", "IPv6", "IPv6" ]. Hosts with an invalid list are ignored.',
    )
    address = String(title="address", description="The full address of the node.")
    country = String(title="country", description="The country where the node can be found.")
    city = String(title="city", description="The city where the node can be found.")
    latitude = Float(title="latitude", description="Geolocation latitude coordinate")
    longitude = Float(title="longitude", description="Geolocation longitude coordinate")
