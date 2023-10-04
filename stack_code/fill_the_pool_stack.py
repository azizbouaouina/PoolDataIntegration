from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as _alambda,
    aws_iam,
    aws_events,
    aws_events_targets,
    aws_lambda_event_sources as event_sources,
    aws_secretsmanager as secretsmanager,
    SecretValue
)


class FillThePoolStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Creating IAM role for lambda
        lambda_s3_cross_account_role = aws_iam.Role(
            self, 
            id="lambda_s3_cross_account_role",
            assumed_by=aws_iam.ServicePrincipal(service="lambda.amazonaws.com"),
            role_name="lambda_s3_cross_account_role",
            inline_policies={
                "AWSBasicExecutionRoles":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],
                                resources=["*"]
                            )
                        ]
                    ),
                "AWSLambdaS3ExecutionRole":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["s3:GetObject"],
                                resources=["*"]
                            )
                        ]
                    ),
                "AWSLambdaSecretsManagerExecutionRole":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["secretsmanager:GetSecretValue"],
                                resources=["*"]
                            )
                        ]
                    )
            }
        )


        fill_the_pool_lambda = _alambda.PythonFunction(
            self,
            id = "fill_the_pool_lambda",
            entry="./lambda_code/",
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="index2.py",
            handler="lambda_handler",
            role = lambda_s3_cross_account_role,
            timeout=Duration.minutes(1),
            function_name="fill_the_pool_lambda"
        )
        
        fill_the_pool_lambda.add_permission(
            "MyResourceBasedPolicy",
            principal=aws_iam.ServicePrincipal('s3.amazonaws.com'),
            action='lambda:InvokeFunction',
            source_arn="arn:aws:s3:::fill-the-pool-data-deliverybucket-9xqeyo7qspbs",
            source_account = "589998742447"
        )


