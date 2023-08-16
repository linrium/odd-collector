import pytest
from odd_models import DataEntity
from odd_models.models import DataEntityType

from tests.integration.helpers import find_by_type

from odd_collector.adapters.duckdb.adapter import Adapter
from odd_collector.domain.plugin import DuckDBPlugin
from odd_collector.adapters.duckdb.mappers.models import DuckDBTable


@pytest.mark.integration
def test_duckdb():
    config = DuckDBPlugin(
        type="duckdb",
        name="duckdb_adapter",
        paths=["./data2.duckdb"],
    )
    data_entities = Adapter(config).get_data_entity_list()
    print(data_entities)
