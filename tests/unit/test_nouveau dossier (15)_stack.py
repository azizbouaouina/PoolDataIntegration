import aws_cdk as core
import aws_cdk.assertions as assertions

from nouveau dossier (15).nouveau dossier (15)_stack import NouveauDossier (15)Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in nouveau dossier (15)/nouveau dossier (15)_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = NouveauDossier (15)Stack(app, "nouveau-dossier--15-")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
