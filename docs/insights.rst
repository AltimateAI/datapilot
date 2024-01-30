Insights
========

The following insights are available in DataPilot:

+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| Name                                  | Type           | Description                                                                                                                                                                                                                                                         | Files Required         | Overrides                   |
+=======================================+================+=====================================================================================================================================================================================================================================================================+========================+=============================+
| source_staging_model_integrity        | Modelling      | Ensures each source has a dedicated staging model and is not directly joined to downstream models.                                                                                                                                                                  | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| downstream_source_dependence          | Modelling      | Evaluates if downstream models (marts or intermediates) are improperly dependent directly on a source. This check ensures that all downstream models depend on staging models, not directly on the source nodes.                                                    | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| Duplicate_Sources                     | Modelling      | Identifies cases where multiple source nodes in a dbt project refer to the same database object. Ensures that each database object is represented by a single, unique source node.                                                                                  | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| hard_coded_references                 | Modelling      | Identifies instances where SQL code within models contains hard-coded references, which can obscure data lineage and complicate project maintenance.                                                                                                                | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| rejoining_upstream_concepts           | Modelling      | Detects scenarios where a parent’s direct child is also a direct child of another one of the parent’s direct children, indicating potential loops or unnecessary complexity in the DAG.                                                                             | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| model_fanout                          | Modelling      | Assesses parent models to identify high fanout scenarios, which may indicate opportunities for more efficient transformations in the BI layer or better positioning of common business logic upstream in the data pipeline.                                         | Manifest               | max_fanout                  |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| multiple_sources_joined               | Modelling      | Checks if a model directly joins multiple source tables, encouraging the use of a single staging model per source for downstream models to enhance data consistency and maintainability.                                                                            | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| root_model                            | Modelling      | Identifies models without direct parents, either sources or other models within the dbt project. Ensures all models can be traced back to a source or interconnected within the project, which is crucial for clear data lineage and project integrity.             | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| source_fanout                         | Modelling      | Evaluates sources for high fanout, identifying when a single source has a large number of direct child models. High fanout may indicate an overly complex or source-reliant data model, potentially introducing risks and complicating maintenance and scalability. | Manifest               | max_fanout                  |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| staging_models_dependency             | Modelling      | Checks whether staging models depend on downstream models, rather than on source or raw data models. Staging models should ideally depend on upstream data sources to maintain a clear and logical data flow.                                                       | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| staging_models_on_staging             | Modelling      | Checks if staging models are dependent on other staging models instead of on source or raw data models, ensuring that staging models are used appropriately to maintain a clear and logical data flow from sources to staging.                                      | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| unused_sources                        | Modelling      | Identifies sources that are defined in the project’s YML files but not used in any models or sources. They may have become redundant due to model deprecation, contributing to unnecessary complexity and clutter in the dbt project.                               | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| chain_view_linking                    | Performance    | Analyzes the dbt project to identify long chains of non-materialized models (views and ephemerals). Such long chains can result in increased runtime for models built on top of them due to extended computation and memory usage.                                  | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| exposure_parent_bad_materialization   | Performance    | Evaluates the materialization types of parent models of exposures to ensure they rely on transformed dbt models or metrics rather than raw sources, and checks if these parent models are materialized efficiently for performance in downstream systems.           | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| documentation_on_stale_columns        | Governance     | Checks for columns that are documented in the dbt project but have been removed from their respective models.                                                                                                                                                       | Manifest, Catalog      | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| exposures_dependent_on_private_models | Governance     | Detects if exposures in the dbt project are dependent on private models. Recommends using public, well-documented, and contracted models as trusted data sources for downstream consumption.                                                                        | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| public_models_without_contracts       | Governance     | Identifies public models in the dbt project that are accessible to all downstream consumers but lack contracts specifying data types and columns.                                                                                                                   | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| missing_documentation                 | Governance     | Detects columns and models that don’t have documentation.                                                                                                                                                                                                           | Manifest, Catalog      | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| undocumented_public_models            | Governance     | Identifies models in the dbt project that are marked as public but don’t have documentation.                                                                                                                                                                        | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| missing_primary_key_tests             | Tests          | Identifies dbt models in the project that lack primary key tests, which are crucial for ensuring data integrity and correctness.                                                                                                                                    | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| dbt_low_test_coverage                 | Tests          | Identifies dbt models in the project that have tests coverage percentage below the required threshold.                                                                                                                                                              | Manifest               | min_test_coverage_percent   |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| model_directory_structure             | Structure      | Checks for correct placement of models in their designated directories. Proper directory structure is essential for organization, discoverability, and maintenance within the dbt project.                                                                          | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| model_naming_convention_check         | Structure      | Ensures all models adhere to a predefined naming convention. A consistent naming convention is crucial for clarity, understanding of the model's purpose, and enhancing navigation within the dbt project.                                                          | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| source_directory_structure            | Structure      | Verifies if sources are correctly placed in their designated directories. Proper directory placement for sources is important for organization and easy searchability.                                                                                              | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+
| test_directory_structure              | Structure      | Checks if tests are correctly placed in the same directories as their corresponding models. Co-locating tests with models aids in maintainability and clarity.                                                                                                      | Manifest               | None                        |
+---------------------------------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+-----------------------------+