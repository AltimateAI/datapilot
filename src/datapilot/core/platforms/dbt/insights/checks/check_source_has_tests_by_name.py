from typing import List
from typing import Tuple

from datapilot.config.utils import get_source_test_name_configuration
from datapilot.core.insights.utils import get_severity
from datapilot.core.platforms.dbt.insights.checks.base import ChecksInsight
from datapilot.core.platforms.dbt.insights.schema import DBTInsightResult
from datapilot.core.platforms.dbt.insights.schema import DBTModelInsightResponse
from datapilot.core.platforms.dbt.schemas.manifest import AltimateResourceType
from datapilot.utils.formatting.utils import numbered_list


class CheckSourceHasTestsByName(ChecksInsight):
    NAME = "Check Source Has Tests By Name"
    ALIAS = "check_source_has_tests_by_name"
    DESCRIPTION = "Check if the source has tests with the specified names"
    REASON_TO_FLAG = (
        "The source table is missing tests with the specified names. Ensure that the source table has tests with the specified names."
    )

    def generate(self, *args, **kwargs) -> List[DBTModelInsightResponse]:
        insights = []
        self.test_names = get_source_test_name_configuration(self.config)
        for node_id, node in self.nodes.items():
            if self.should_skip_model(node_id):
                self.logger.debug(f"Skipping model {node_id} as it is not enabled for selected models")
                continue
            if node.resource_type == AltimateResourceType.source:
                if self._source_has_tests_by_name(node_id, self.test_names):
                    insights.append(
                        DBTModelInsightResponse(
                            unique_id=node_id,
                            package_name=node.package_name,
                            path=node.original_file_path,
                            original_file_path=node.original_file_path,
                            insight=self._build_failure_result(node_id, self.test_names),
                            severity=get_severity(self.config, self.ALIAS, self.DEFAULT_SEVERITY),
                        )
                    )
        return insights

    def _build_failure_result(self, source_unique_id: str, test_names: List[str]) -> DBTInsightResult:
        failure_message = (
            "The source table `{source_unique_id}` is missing the following tests: {test_names}. "
            "Ensure that the source table has the required tests."
        )
        recommendation = (
            "Add the following tests to the source table `{source_unique_id}`: {test_names}. "
            "Ensuring that the source table has the required tests helps in maintaining data integrity and consistency."
        )
        return DBTInsightResult(
            failure_message=failure_message.format(source_unique_id=source_unique_id, test_names=numbered_list(test_names)),
            recommendation=recommendation.format(source_unique_id=source_unique_id, test_names=numbered_list(test_names)),
            metadata={"source_unique_id": source_unique_id, "test_names": test_names},
        )

    def _source_has_tests_by_name(self, source_id, test_names: List[str]) -> bool:
        source = self.get_node(source_id)
        source_test_metadata = source.test_metadata
        if source_test_metadata.name in test_names:
            return True
        return False

    @classmethod
    def has_all_required_data(cls, has_manifest: bool, has_catalog: bool, **kwargs) -> Tuple[bool, str]:
        if not has_manifest:
            return False, "Manifest is required for insight to run."

        if not has_catalog:
            return False, "Catalog is required for insight to run."

        return True, ""
