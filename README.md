
# Azure Remediation Project

This repository contains code for handling and remediating Azure events using the Azure Python SDK.

## About the Project

This project includes three classes, each corresponding to a specific Azure event:

1. `CryptoMiningIP`: Handles events related to communication with crypto-mining IPs.
2. `EnforceDataBaseEncryption`: Handles events related to enforcing encryption of data in transit.
3. `ExposedDatabase`: Handles events related to databases exposed by firewall rules.

Each class uses the Azure Python SDK to interact with Azure services and remediate the events.


### Prerequisites

This project requires Python 3.11. Make sure you have this version installed before running the project. You can check your Python version using the following command:

```bash
python --version
```

To use the Azure-python sdk, you need to have the following:

1. An Azure account. If you don't have one, you can create a free account [here](https://azure.microsoft.com/free/).
2. The Azure CLI installed. You can download it [here](https://docs.microsoft.com/cli/azure/install-azure-cli).
3. The `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET` environment variables set. These values are used for authentication.

## Azure Permissions

To use this project, you need the following permissions in Azure:

1. `Microsoft.Network/networkSecurityGroups/write`: This permission is required to modify network security groups, which is necessary for the `CryptoMiningIP` and `ExposedDatabase` classes.
2. `Microsoft.Compute/virtualMachines/write`: This permission is required to modify virtual machines, which is necessary for the `CryptoMiningIP` class.
3. `Microsoft.Sql/servers/firewallRules/write`: This permission is required to modify SQL server firewall rules, which is necessary for the `ExposedDatabase` class.
4. `Microsoft.Storage/storageAccounts/update`: This permission is required to update storage accounts, which is necessary for the `EnforceDataBaseEncryption` class.

Make sure you have these permissions before running the project. If you don't have these permissions, you'll need to ask your Azure administrator to grant them to you.

## Installation

This project requires specific versions of certain Python packages to run correctly. These packages are listed in the `requirements.txt` file.

To install these packages, you can use the following command:

```bash
pip install -r requirements.txt
```

## Running the Code

Before running the code, make sure to authenticate with Azure by running the following command in your terminal:

```bash
az login
```
