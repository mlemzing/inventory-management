from aws_cdk import CfnOutput, Stack
from aws_cdk.aws_dynamodb import Table, TableEncryption, AttributeType, ProjectionType
from constructs import Construct


class DatabaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table = Table(
            self,
            "ProductTable",
            # PK is the id of the item
            partition_key={"name": "id", "type": AttributeType.STRING},
            encryption=TableEncryption.AWS_MANAGED,
            point_in_time_recovery=True,
            deletion_protection=False
        )

        self.table.add_global_secondary_index(
            index_name="ItemNameIndex",
            partition_key={"name": "item_name", "type": AttributeType.STRING},
            projection_type=ProjectionType.ALL
        )
        self.table.add_global_secondary_index(
            index_name="CategoryIndex",
            partition_key={"name": "category", "type": AttributeType.STRING},
            projection_type=ProjectionType.ALL
        )
        # self.table.add_global_secondary_index(
        #     index_name="LastUpdatedAtIndex",
        #     partition_key={"name": "last_updated_at",
        #                    "type": AttributeType.STRING},
        #     projection_type=ProjectionType.ALL
        # )
        self.table.add_global_secondary_index(
            index_name="IDToLastUpdatedAtIndex",
            partition_key={"name": "id", "type": AttributeType.STRING},
            sort_key={"name": "last_updated_at",
                      "type": AttributeType.STRING},
            projection_type=ProjectionType.ALL
        )

        CfnOutput(self, "TableName", value=self.table.table_name,
                  export_name="TableName")
