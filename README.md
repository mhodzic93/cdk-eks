# cdk-eks

This repository contains AWS CDK code that deploys an EKS cluster as well as a kubernetes manifest
to deploy a simple hello-world container into the provisioned EKS cluster.

## Pre-Requisites
1. The pre-requisites required for running CDK can be found here: https://cdkworkshop.com/15-prerequisites.html
2. Install kubectl: https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
3. Install jq: https://stedolan.github.io/jq/download/

## Step by Step Deployment
1. Clone this repository locally.

2. Activate the Virtualenv by running the following commands:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Once the Virtualenv is activated, install the required dependencies.
    ```
    pip install -r requirements.txt
    ```

4. Synthesize the CloudFormation template. Replace `ACCOUNT` with your AWS Account ID and replace `REGION`
   with the AWS region that you are deploying into.
    ```
    cdk synth --context ACCOUNT=<ACCOUNT> --context REGION=<REGION>
    ```

5. Deploy the CDK Toolkit stack. Replace `ACCOUNT` with your AWS Account ID and replace `REGION`
   with the AWS region that you are deploying into.
    ```
    cdk bootstrap aws://<ACCOUNT>/<REGION>
    ```

6. Deploy the stack. Replace `ACCOUNT` with your AWS Account ID and replace `REGION`
   with the AWS region that you are deploying into. When prompted if you wish to deploy
   the changes, enter `y` to deploy.
   ```
   cdk deploy
   ```

7. When you have deployed the stack, you will see an output containing a command to update
   kubeconfig. Copy this command and execute it. If this command was executed successfully, you 
   should receive a response similar to: 
    ```
    Updated context arn:aws:eks:<REGION>:<ACCOUNT_ID>:cluster/<CLUSTER_NAME> in ~/.kube/config
    ```

8. Verify that you are now able to use kubectl by running:
    ```
    kubectl get nodes
    ```

9. Deploy the hello-world application into the cluster:
    ```
    kubectl apply -f ./manifest.yaml 
    ```

10. Create a Service object to exposes the deployment:
    ```
    kubectl expose deployment hello-world --type=LoadBalancer --name=load-balancer
    ```

11. Get the external IP address and the port and navigate to the site to verify the service has been
    deployed successfully:
    ```
    ADDRESS=$(kubectl get service load-balancer -o json | jq -r '.status.loadBalancer.ingress[].hostname')
    PORT=$(kubectl get service load-balancer -o json | jq -r '.spec.ports[].port')
    curl -v http://{$ADDRESS}:{$PORT}
    ```
 