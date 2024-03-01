from typing import List

from datapilot.config.utils import get_blacklist_schema_configuration
from datapilot.config.utils import get_whitelist_schema_configuration
from datapilot.core.insights.utils import get_severity
from datapilot.core.platforms.dbt.insights.checks.base import ChecksInsight
from datapilot.core.platforms.dbt.insights.schema import DBTInsightResult
from datapilot.core.platforms.dbt.insights.schema import DBTModelInsightResponse
from datapilot.core.platforms.dbt.schemas.manifest import AltimateResourceType


class CheckModelParentsSchema(ChecksInsight):
    NAME = "Check Model Parents Schema"
    ALIAS = "check_model_parents_schema"
    DESCRIPTION = "Ensures the parent models or sources are from certain schema."
    REASON_TO_FLAG = "The model has a different schema as parent model or source."

    def _build_failure_result(
        self,
        node_id: str,
        parent_schema: str,
    ) -> DBTInsightResult:
        """
        Build failure result for the insight if a model's parent schema is not whitelist or in blacklist.
        """

        failure_message = f"The model:{node_id}'s parent model's schema is not in whitelist or blacklisted:\n"

        recommendation = "Update the parent model's schema to adhere to the whitelist or remove the model from the blacklist."

        return DBTInsightResult(
            type=self.TYPE,
            name=self.NAME,
            message=failure_message,
            recommendation=recommendation,
            reason_to_flag=self.REASON_TO_FLAG,
            metadata={"parent_schema": parent_schema},
        )

    def generate(self, *args, **kwargs) -> List[DBTModelInsightResponse]:
        """
        Generate a list of InsightResponse objects for each model in the DBT project,
        ensures the parent models or sources are from certain schema.
        The whitelist and blacklist of schemas are defined in the config file.
        """
        insights = []
        self.whitelist = get_whitelist_schema_configuration(self.config)
        self.blacklist = get_blacklist_schema_configuration(self.config)
        self.blacklist = self.blacklist if self.blacklist else []
        for node_id in self.nodes.keys():
            if self.should_skip_model(node_id):
                self.logger.debug(f"Skipping model {node_id} as it is not enabled for selected models")
                continue
            parent_schema = self._check_model_parents_schema(node_id)
            if parent_schema:
                insights.append(
                    DBTModelInsightResponse(
                        unique_id=node_id,
                        package_name=self.nodes[node_id].package_name,
                        path=self.nodes[node_id].original_file_path,
                        original_file_path=self.nodes[node_id].original_file_path,
                        insight=self._build_failure_result(node_id, parent_schema),
                        severity=get_severity(self.nodes[node_id].resource_type),
                    )
                )
        return insights

    def _check_model_parents_schema(self, model_unique_id: str) -> bool:
        """
        Check if the parent models or sources are from certain schema.
        """
        model = self.get_node(model_unique_id)
        if model.resource_type == AltimateResourceType.model:
            for parent in getattr(model.depends_on, "nodes", []):
                parent_model = self.get_node(parent)
                if (self.whitelist and (parent_model.schema_name not in self.whitelist)) or (parent_model.schema in self.blacklist):
                    return parent_model.schema_name
        return None
