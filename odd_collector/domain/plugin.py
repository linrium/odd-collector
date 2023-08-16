from pathlib import Path
from typing import List, Literal, Optional

from odd_collector_sdk.domain.plugin import Plugin as BasePlugin
from odd_collector_sdk.types import PluginFactory

from odd_collector.domain.predefined_data_source import PredefinedDatasourceParams


class WithPredefinedDataSource:
    predefined_datasource: PredefinedDatasourceParams


class WithHost(BasePlugin):
    host: str


class WithPort(BasePlugin):
    port: str


class DuckDBPlugin(BasePlugin):
    type: Literal["duckdb"]
    paths: list[Path]
    host: Optional[str] = "localhost"


PLUGIN_FACTORY: PluginFactory = {
    "duckdb": DuckDBPlugin,
}
