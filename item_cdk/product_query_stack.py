from aws_cdk import Fn, Stack
from aws_cdk.aws_apigatewayv2 import HttpMethod
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_iam import PolicyStatement
from constructs import Construct

from item_cdk.http_api_stack import HttpApiStack
from item_cdk.database_stack import DatabaseStack


class ProductQueryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, http_api_stack: HttpApiStack, database_stack: DatabaseStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table_name = Fn.import_value("TableName")

        self.query_function = Function(
            self, "InventoryQueryFunction",
            runtime=Runtime.PYTHON_3_8,
            handler="read.lambda_handler",
            code=Code.from_asset("lambda/inventory"),
            environment={
                'TABLE_NAME': table_name
            }
        )
        self.query_function.add_to_role_policy(
            PolicyStatement(
                actions=["dynamodb:Scan"],
                resources=[database_stack.table.table_arn]
            )
        )
        database_stack.table.grant_read_write_data(self.query_function)

        http_api_stack.http_api.add_routes(
            path="/inventory",
            methods=[HttpMethod.GET],
            integration=HttpLambdaIntegration(
                "InventoryQueryIntegration",
                handler=self.query_function,
            )
        )
