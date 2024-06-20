from aws_cdk import Fn, Stack
from aws_cdk.aws_apigatewayv2 import HttpMethod
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_iam import PolicyStatement
from constructs import Construct

from item_cdk.http_api_stack import HttpApiStack
from item_cdk.database_stack import DatabaseStack


class ProductCreateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, http_api_stack: HttpApiStack, database_stack: DatabaseStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table_name = Fn.import_value("TableName")

        self.create_function = Function(
            self, "InventoryCreate",
            runtime=Runtime.PYTHON_3_8,
            handler="create.lambda_handler",
            code=Code.from_asset("lambda/inventory"),
            environment={
                'TABLE_NAME': table_name
            }
        )
        self.create_function.add_to_role_policy(
            PolicyStatement(
                actions=["dynamodb:PutItem"],
                resources=[database_stack.table.table_arn]
            )
        )
        database_stack.table.grant_read_write_data(self.create_function)

        http_api_stack.http_api.add_routes(
            path="/inventory",
            methods=[HttpMethod.POST],
            integration=HttpLambdaIntegration(
                "InventoryCreateIntegration",
                handler=self.create_function,
            )
        )
