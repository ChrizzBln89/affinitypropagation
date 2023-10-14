from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
    AssetSelection,
    sensor,
    RunRequest,
)

from . import assets

all_assets = load_assets_from_modules([assets])
upload_job = define_asset_job("upload_job", selection=AssetSelection.all())
asset_job = define_asset_job(name="asset_job", selection="get_symbols")


@sensor(job=upload_job, minimum_interval_seconds=60 * 10)
def materializes_asset_sensor():
    yield RunRequest()


defs = Definitions(
    assets=all_assets, jobs=[upload_job, asset_job], sensors=[materializes_asset_sensor]
)
