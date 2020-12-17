import os
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_eks as eks,
    core,
)
from aws_cdk.core import Environment


class EksCluster(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)

        eks_cluster = eks.Cluster(self, "EksCluster",
                                  cluster_name="eks-cluster",
                                  # managed by ASG
                                  default_capacity=0,
                                  kubectl_enabled=True,
                                  version=eks.KubernetesVersion.V1_17,
                                  vpc=vpc,
                                  # default vpc only has public subnets
                                  vpc_subnets=vpc.select_subnets(
                                      subnet_type=ec2.SubnetType.PUBLIC, one_per_az=True).subnets
                                  )

        asg = autoscaling.AutoScalingGroup(self, "EksASG",
                                           min_capacity=1,
                                           max_capacity=2,
                                           instance_type=ec2.InstanceType("t3.small"),
                                           machine_image=eks.EksOptimizedImage(
                                               kubernetes_version="1.17"
                                           ),
                                           update_type=autoscaling.UpdateType.ROLLING_UPDATE,
                                           vpc=vpc
                                           )

        node_group = eks.Nodegroup(self, "NodeGroup",
                                   nodegroup_name="eks-worker",
                                   cluster=eks_cluster,
                                   instance_type=ec2.InstanceType("t3.small"),
                                   min_size=1,
                                   max_size=2,
                                   tags={"Name": "eks-worker"}
                                   )


app = core.App()
# set variables for environment
ACCOUNT = app.node.try_get_context("ACCOUNT") or os.environ.get("CDK_DEFAULT_ACCOUNT")
REGION = app.node.try_get_context("REGION") or os.environ.get("CDK_DEFAULT_REGION")
ENV = Environment(region=REGION, account=ACCOUNT)

EksCluster(app, "EksCluster", env=ENV)
app.synth()
