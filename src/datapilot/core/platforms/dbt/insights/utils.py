from datapilot.core.platforms.dbt.insights import INSIGHTS


def get_insight_with_configs():
    return [insight.get_config_schema() for insight in INSIGHTS]
