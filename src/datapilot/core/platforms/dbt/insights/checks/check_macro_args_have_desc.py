from typing import List
from typing import Tuple

from datapilot.core.insights.utils import get_severity
from datapilot.core.platforms.dbt.insights.checks.base import ChecksInsight
from datapilot.core.platforms.dbt.insights.schema import DBTInsightResult
from datapilot.core.platforms.dbt.insights.schema import DBTModelInsightResponse
from datapilot.core.platforms.dbt.schemas.manifest import AltimateResourceType


class CheckMacroArgsHaveDesc(ChecksInsight):
    NAME = "Check Macro Args Have Desc"
    ALIAS = "check_macro_args_have_desc"
    DESCRIPTION = (
        "Checks that macros have descriptions for their arguments. Descriptions help in understanding the purpose of the macro arguments."
    )
    REASON_TO_FLAG = "Macros without descriptions for their arguments can lead to confusion and hinder effective data modeling and analysis. It's important to have descriptions for macro arguments."

    def _build_failure_result(
        self,
        node_id: str,
    ) -> DBTInsightResult:
        """
        Build failure result for the insight if a macro doesn't have a description.

        :return: An instance of InsightResult containing failure message and recommendation.
        """

        failure_message = f"The macro `{node_id}` does not have a description."
        recommendation = "Add a description to the macro to help in understanding the purpose of the macro."

        return DBTInsightResult(
            type=self.TYPE,
            name=self.NAME,
            message=failure_message,
            recommendation=recommendation,
            reason_to_flag=self.REASON_TO_FLAG,
        )

    def generate(self, *args, **kwargs) -> List[DBTModelInsightResponse]:
        """
        Generate a list of InsightResponse objects for each model in the DBT project,
        identifying macros whose arguments don't have descriptions.
        :return: A list of InsightResponse objects.
        """

        insights = []
        for node_id, node in self.nodes.items():
            if self.should_skip_model(node_id):
                self.logger.debug(f"Skipping model {node_id} as it is not enabled for selected models")
                continue
            if node.resource_type == AltimateResourceType.macro:
                if not self._check_macro_args_have_desc(node_id):
                    insights.append(
                        DBTModelInsightResponse(
                            node_id=node_id,
                            result=self._build_failure_result(node_id),
                            severity=get_severity(self.TYPE, self.config),
                        )
                    )

        return insights

    def _check_macro_args_have_desc(self, node_id) -> bool:
        """
        Check if the macro has descriptions for its arguments.
        Assuming that macro.columns contains the arguments of the macro. Might not be th case
        """
        macro = self.get_node(node_id)
        for arg in macro.columns.values():
            if not arg.description:
                return False
        return True

    @classmethod
    def has_all_required_data(cls, has_manifest: bool, has_catalog: bool, **kwargs) -> Tuple[bool, str]:
        return True, ""
