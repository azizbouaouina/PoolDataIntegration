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


class TemperatureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create the s3 bucket
        bucket_temperature = s3.Bucket(self, 
                           id = "temperature-bucket-aziz",
                           bucket_name="temperature-bucket-aziz",
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                           )

        put_temperature_function = _alambda.PythonFunction(
            self,
            id = "put_temperature_function",
            entry="./lambda_code/",
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="index3.py",
            handler="lambda_handler",
            role = aws_iam.Role.from_role_arn(self,
                                              "role_id", 
                                              role_arn="arn:aws:iam::639311385687:role/lambda_execution_role"
            ),
            function_name="put_temperature_function"
        )

        rule = aws_events.Rule(
            self,
            id="temperature_schedule",
            schedule= aws_events.Schedule.rate(Duration.hours(1))
        )
        rule.add_target(aws_events_targets.LambdaFunction(handler=put_temperature_function))


        clickhouse_temperature_function = _alambda.PythonFunction(
            self,
            id = "clickhouse_temperature_function",
            entry="./lambda_code/",
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="index4.py",
            handler="lambda_handler",
            role = aws_iam.Role.from_role_arn(self,
                                              "role_id_get_obj", 
                                              role_arn="arn:aws:iam::639311385687:role/lambda_execution_role_get_object"
            ),
            function_name="clickhouse_temperature_function"
        )

        clickhouse_temperature_function.add_event_source(event_sources.S3EventSource(bucket_temperature,
                                                                       events=[s3.EventType.OBJECT_CREATED_PUT]
                                                                       )
                                            )



