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
from item_cdk.product_create_stack import ProductCreateStack
from item_cdk.product_query_stack import ProductQueryStack
from item_cdk.product_category_query_stack import ProductCategoryQueryStack
from item_cdk.category_list_stack import CategoryListStack
from item_cdk.product_filter_stack import ProductFilterStack


class ItemCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._database_stack = DatabaseStack(self, "DatabaseStack")
        self._http_api_stack = HttpApiStack(self, "HttpApiStack")
        self._product_create_stack = ProductCreateStack(
            self, "RoutesStack", self._http_api_stack, self._database_stack)
        self._product_query_stack = ProductQueryStack(
            self, "ProductQueryStack", self._http_api_stack, self._database_stack)
        self._product_category_query_stack = ProductCategoryQueryStack(
            self, "ProductCategoryQueryStack", self._http_api_stack, self._database_stack)
        self._category_list_stack = CategoryListStack(
            self, "CategoryListStack", self._http_api_stack, self._database_stack)
        self._product_filter_stack = ProductFilterStack(
            self, "ProductFilterStack", self._http_api_stack, self._database_stack)
