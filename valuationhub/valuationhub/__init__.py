from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
    AssetSelection,
)

from . import assets

all_assets = load_assets_from_modules([assets])
upload_job = define_asset_job("upload_job", selection=AssetSelection.all())

defs = Definitions(assets=all_assets, jobs=[upload_job])
