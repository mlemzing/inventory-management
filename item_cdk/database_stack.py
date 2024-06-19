from aws_cdk import Stack
from aws_cdk.aws_dynamodb import Table, TableEncryption, AttributeType
from constructs import Construct


class DatabaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table = Table(
            self,
            "InventoryTable",
            partition_key={"name": "id", "type": AttributeType.STRING},
            sort_key={"name": "last_updated_dt", "type": AttributeType.STRING},
            encryption=TableEncryption.AWS_MANAGED,
            point_in_time_recovery=True,
            deletion_protection=True
        )
