
## Introduction

DataPilot is an AI teammate for engineers to ensure best practices in their SQL and dbt projects. DataPilot can be integrated into local environments to help identify potential issues early. It can also be integrated into Git and CI/CD to ensure certain standards are followed for data projects at the organizational level.

Here are a few key insights, the full list of insights is available below.

1. High Source or model fanouts
2. Hard code references
3. Unused or duplicate sources
4. Downstream / source / staging model dependency checks
5. Missing tests or documentation

### Setup

Required Python Version: Python 3.7 or higher.

DataPilot is available as a Python package and can be easily installed using pip.

```Shell
pip install altimate-datapilot
```

### Usage

To check the project health of your dbt project, use the following command in the format below:

```shell
datapilot dbt project-health --manifest-path [path_to_manifest] --catalog-path [path_to_catalog] --config-path [path_to_config]
```
Replace [path_to_manifest] and [path_to_catalog] with the actual paths to your dbt project's manifest and catalog files. These files are typically generated by dbt and contain essential metadata about your dbt project.

The [--catalog-path] is an optional argument. If you don't specify a catalog path, the tool will skip some insights that require the catalog file.

The [--config-path] is an optional argument. You can provide a yaml file with overrides for the default behavior of the insights.

#### Generating Manifest and Catalog Files for dbt Projects

1. Generate Manifest File (manifest.json). Open your dbt project's root directory in a terminal or command prompt. Run `dbt compile`. This command generates manifest.json in the target folder under your dbt project directory structure.

2. Generate Catalog File (catalog.json). Ensure you're in your dbt project's root directory. Run `dbt docs generate`. This command generates catalog.json.json in the target folder under your dbt project directory structure

Note: The dbt docs generate requires an active database connection and may take a long time for projects with large number of models.

### Checks

The following checks are available:

| Name                           | Type       | Description                                                                                                                                                                 | Files Required         | Overrides                  |
|--------------------------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|----------------------------|
| source_staging_model_integrity | Modelling  | Ensures each source has a dedicated staging model and is not directly joined to downstream models                                                                             | Manifest File          | None                       |
| downstream_source_dependence   | Modelling  | Evaluates if downstream models (marts or intermediates) are improperly dependent directly on a source. This check ensures that all downstream models depend on staging models, not directly on the source nodes. | Manifest File          | None                       |
| Duplicate_Sources              | Modelling  | Identifies cases where multiple source nodes in a dbt project refer to the same database object. Ensures that each database object is represented by a single, unique source node. | Manifest File          | None                       |
| hard_coded_references          | Modelling  | Identifies instances where SQL code within models contains hard-coded references, which can obscure data lineage and complicate project maintenance.                          | Manifest File          | None                       |
| rejoining_upstream_concepts    | Modelling  | Detects scenarios where a parent’s direct child is also a direct child of another one of the parent’s direct children, indicating potential loops or unnecessary complexity in the DAG. | Manifest File          | None                       |
| model_fanout                   | Modelling  | Assesses parent models to identify high fanout scenarios, which may indicate opportunities for more efficient transformations in the BI layer or better positioning of common business logic upstream in the data pipeline. | Manifest File          | - max_fanout               |
| multiple_sources_joined        | Modelling  | Checks if a model directly joins multiple source tables, encouraging the use of a single staging model per source for downstream models to enhance data consistency and maintainability. | Manifest File          | None                       |
| root_model                     | Modelling  | Identifies models without direct parents, either sources or other models within the dbt project. Ensures all models can be traced back to a source or interconnected within the project, which is crucial for clear data lineage and project integrity. | Manifest File          | None                       |
| source_fanout                  | Modelling  | Evaluates sources for high fanout, identifying when a single source has a large number of direct child models. High fanout may indicate an overly complex or source-reliant data model, potentially introducing risks and complicating maintenance and scalability. | Manifest File          | - max_fanout               |
| staging_models_dependency      | Modelling  | Checks whether staging models depend on downstream models, rather than on source or raw data models. Staging models should ideally depend on upstream data sources to maintain a clear and logical data flow. | Manifest File          | None                       |
| staging_models_on_staging      | Modelling  | Checks if staging models are dependent on other staging models instead of on source or raw data models, ensuring that staging models are used appropriately to maintain a clear and logical data flow from sources to staging. | Manifest File          | None                       |
| unused_sources                 | Modelling  | Identifies sources that are defined in the project’s YML files but not used in any models or sources. They may have become redundant due to model deprecation, contributing to unnecessary complexity and clutter in the dbt project. | Manifest File          | None                       |
| chain_view_linking             | Performance | Analyzes the dbt project to identify long chains of non-materialized models (views and ephemerals). Such long chains can result in increased runtime for models built on top of them due to extended computation and memory usage. | Manifest File          | None                       |
| exposure_parent_bad_materialization | Performance | Evaluates the materialization types of parent models of exposures to ensure they rely on transformed dbt models or metrics rather than raw sources, and checks if these parent models are materialized efficiently for performance in downstream systems. | Manifest File          | None                       |
| documentation_on_stale_columns | Governance | Checks for columns that are documented in the dbt project but have been removed from their respective models                                                               | Manifest File, Catalog File | None                       |
| exposures_dependent_on_private_models | Governance | Detects if exposures in the dbt project are dependent on private models. Recommends using public, well-documented, and contracted models as trusted data sources for downstream consumption | Manifest File          | None                       |
| public_models_without_contracts | Governance | Identifies public models in the dbt project that are accessible to all downstream consumers but lack contracts specifying data types and columns.                           | Manifest File          | None                       |
| missing_documentation          | Governance | Detects columns and models that don’t have documentation                                                                                                                     | Manifest File, Catalog File | None                       |
| undocumented_public_models     | Governance | Identifies models in the dbt project that are marked as public but don’t have documentation                                                                                 | Manifest File          | None                       |
| missing_primary_key_tests      | Tests      | Identifies dbt models in the project that lack primary key tests, which are crucial for ensuring data integrity and correctness.                                            | Manifest File          | None                       |
| dbt_low_test_coverage          | Tests      | Identifies dbt models in the project that have tests coverage percentage below the required threshold.                                                                       | Manifest File          | min_test_coverage_percent |

## Configuration

For DataPilot, you can tailor the behavior of the insights by adjusting their configurations. This is done using a YAML configuration file. You can set severity levels for different insights, disable specific insights, or provide specific overrides.

### YAML Configuration Structure

Here’s an example of configurations that can be specific in YAML file:

```yaml
version: v1

# Insights to disable
disabled_insights:
  - source_staging_model_integrity
  - downstream_source_dependence
  - Duplicate_Sources
  - hard_coded_references
  - rejoining_upstream_concepts
  - model_fanout
  - multiple_sources_joined

# Define patterns to identify different types of models
model_type_patterns:
  staging: "^stg_.*"       # Regex for staging models
  mart: "^(mrt_|mart_|fct_|dim_).*"  # Regex for mart models
  intermediate: "^int_.*"  # Regex for intermediate models
  base: "^base_.*"         # Regex for base models

# Configure insights
insights:
  # Set minimum test coverage percent and severity for 'Low Test Coverage in DBT Models'
  dbt_low_test_coverage:
    min_test_coverage_percent: 30
    severity: WARNING

  # Configure maximum fanout for 'Model Fanout Analysis'
  model_fanout.max_fanout: 10

  # Configure maximum fanout for 'Source Fanout Analysis'
  source_fanout.max_fanout: 10

  # Define model types considered as downstream for 'Staging Models Dependency Check'
  staging_models_dependency.downstream_model_types:
    - mart

```

### Key Sections of the config file

- disabled_insights: Insights that you want to disable
- model_type_patterns: Regex patterns to identify different model types like staging, mart, etc.
- insights: Custom configurations for each insight. For each insight, you can set specific thresholds, severity levels, or other parameters.

### Overriding default configs for the insights
- To change the severity level or set a threshold, modify the corresponding insight under the insights section. For example

`Severity` can have 3 values -> `INFO`, `WARNING`, `ERROR`
```
insights:
  dbt_low_test_coverage:
    severity: WARNING
```

- For insights with more complex configurations (like fanout thresholds or model types), you need to specify the insight name and corresponding parameter under insights. For example:
```
insights:
  model_fanout.max_fanout: 10
```
