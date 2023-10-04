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


class OndiloStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create the s3 bucket
        bucket = s3.Bucket(self, 
                           id = "ondilo-bucket-aziz",
                           bucket_name="ondilo-bucket-aziz",
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                           )


        # Creating IAM role for lambda
        lambda_execution_role = aws_iam.Role(
            self, 
            id="lambda__execution_role",
            assumed_by=aws_iam.ServicePrincipal(service="lambda.amazonaws.com"),
            description="This role will be used by the Lambda to put objects into an s3 bucket",
            role_name="lambda_execution_role",
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
                                actions=["s3:PutObject"],
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

        ondilo_function = _alambda.PythonFunction(
            self,
            id = "function",
            entry="./lambda_code/",
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="index.py",
            handler="lambda_handler",
            role = lambda_execution_role,
            function_name="ondilo_function"
        )

        rule = aws_events.Rule(
            self,
            id="lambda_schedule",
            schedule= aws_events.Schedule.rate(Duration.hours(1))
        )
        rule.add_target(aws_events_targets.LambdaFunction(handler=ondilo_function))


        # Creating IAM role for lambda
        lambda_execution_role_get_object = aws_iam.Role(
            self, 
            id="lambda_execution_role_get_object",
            assumed_by=aws_iam.ServicePrincipal(service="lambda.amazonaws.com"),
            description="This role will be used by the Lambda to get objects from an s3 bucket",
            role_name="lambda_execution_role_get_object",
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

        lambda_clickhouse = _alambda.PythonFunction(
            self,
            id = "lambda_clickhouse",
            entry="./lambda_code/",
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="index1.py",
            handler="lambda_handler",
            role = lambda_execution_role_get_object,
            timeout=Duration.minutes(1),
            function_name="clickhouse_function"
        )

        lambda_clickhouse.add_event_source(event_sources.S3EventSource(bucket,
                                                                       events=[s3.EventType.OBJECT_CREATED_PUT]
                                                                       )
                                            )



