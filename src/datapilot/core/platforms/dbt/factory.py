from dbt_artifacts_parser.parsers.catalog.catalog_v1 import CatalogV1
from dbt_artifacts_parser.parsers.manifest.manifest_v9 import ManifestV9
from dbt_artifacts_parser.parsers.manifest.manifest_v10 import ManifestV10
from dbt_artifacts_parser.parsers.manifest.manifest_v11 import ManifestV11

from datapilot.core.platforms.dbt.schemas.manifest import Catalog
from datapilot.core.platforms.dbt.schemas.manifest import Manifest
from datapilot.core.platforms.dbt.wrappers.catalog.v1.wrapper import CatalogV1Wrapper
from datapilot.core.platforms.dbt.wrappers.manifest.v9.wrapper import ManifestV9Wrapper
from datapilot.core.platforms.dbt.wrappers.manifest.v10.wrapper import ManifestV10Wrapper
from datapilot.core.platforms.dbt.wrappers.manifest.v11.wrapper import ManifestV11Wrapper
from datapilot.exceptions.exceptions import AltimateNotSupportedError


class DBTFactory:
    @classmethod
    def get_manifest_wrapper(cls, manifest: Manifest):
        if isinstance(manifest, ManifestV11):
            return ManifestV11Wrapper(manifest)
        if isinstance(manifest, ManifestV10):
            return ManifestV10Wrapper(manifest)
        if isinstance(manifest, ManifestV9):
            return ManifestV9Wrapper(manifest)
        raise AltimateNotSupportedError(f"Manifest version {manifest.metadata.dbt_schema_version} not supported")

    @classmethod
    def get_catalog_wrapper(cls, catalog: Catalog):
        if isinstance(catalog, CatalogV1):
            return CatalogV1Wrapper(catalog)
        raise AltimateNotSupportedError(f"Catalog version {catalog.metadata.dbt_schema_version} not supported")
