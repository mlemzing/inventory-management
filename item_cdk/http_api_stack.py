from aws_cdk import Stack
from aws_cdk.aws_apigatewayv2 import CorsHttpMethod, CorsPreflightOptions, HttpApi
from constructs import Construct


class HttpApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.http_api = HttpApi(
            self,
            "InventoryHttpApi",
            cors_preflight=CorsPreflightOptions(
                allow_origins=["*", "http://localhost:3000"],
                allow_headers=["Authorization"],
                allow_methods=[CorsHttpMethod.POST, CorsHttpMethod.GET,
                               CorsHttpMethod.PUT, CorsHttpMethod.DELETE],
            ),
        )
