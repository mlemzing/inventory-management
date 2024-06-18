from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigatewayv2 as apigateway,
    aws_lambda as _lambda,
)
from constructs import Construct
from item_cdk.database_stack import DatabaseStack
from item_cdk.http_api_stack import HttpApiStack
from item_cdk.routes_stack import RoutesStack


class ItemCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._database_stack = DatabaseStack(self, "DatabaseStack")
        self._http_api_stack = HttpApiStack(self, "HttpApiStack")
        self._routes_stack = RoutesStack(
            self, "RoutesStack", self._http_api_stack, self._database_stack)
