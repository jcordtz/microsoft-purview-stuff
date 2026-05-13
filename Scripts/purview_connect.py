#!/usr/bin/env python3
# ##############################################################################
# ⚠️  WARNING - PLEASE READ BEFORE USING THIS SCRIPT  ⚠️
# ##############################################################################
#
# THIS SCRIPT IS PROVIDED "AS IS" - FOR INSPIRATION AND EDUCATIONAL PURPOSES ONLY
#
# NO WARRANTY: This code comes with absolutely NO WARRANTY or GUARANTEE of any
# kind. It may contain bugs, errors, or security vulnerabilities.
#
# NO SUPPORT: The author(s) provide NO SUPPORT and are under NO OBLIGATION to
# fix issues, answer questions, or provide updates.
#
# USE AT YOUR OWN RISK: You are solely responsible for any consequences arising
# from the use of this script. Test thoroughly before using in any environment.
#
# NOT FOR PRODUCTION: This is sample/demo code. Do NOT use in production without
# thorough review, testing, and modifications per your organization's standards.
#
# ##############################################################################

"""
===============================================================================
Purview Data Governance Connection Script
===============================================================================

OVERVIEW
--------
This script provides a command-line interface for connecting to and interacting
with Microsoft Purview Data Governance. It uses service principal authentication
to establish secure connections and offers various operations such as listing
collections, searching the catalog, and retrieving entity details.

FEATURES
--------
- Service Principal Authentication: Secure authentication using Azure AD
- Flexible Configuration: Load credentials from environment variables or file
- Multiple Operations: Test connection, list collections, search catalog,
  get entity details
- Output Formats: Human-readable text or JSON output
- Lazy Initialization: Clients are created on-demand for optimal resource usage

PREREQUISITES
-------------
Required Python packages:
    pip install azure-identity azure-purview-catalog azure-purview-administration

Azure configuration needed:
    1. Microsoft Purview Account in Azure
    2. Service Principal with Tenant ID, Client ID, and Client Secret
    3. Appropriate Purview permissions (Data Curator/Data Reader role)

CONFIGURATION
-------------
Option 1 - Environment Variables:
    export PURVIEW_NAME=your-purview-account-name
    export AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    export AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    export AZURE_CLIENT_SECRET=your-client-secret

Option 2 - Parameters File (parameters.txt):
    PURVIEW_NAME=your-purview-account-name
    AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    AZURE_CLIENT_SECRET=your-client-secret

Note: Environment variables take precedence over values in the parameters file.

USAGE
-----
Basic connection test:
    python purview_connect.py

Using a parameters file:
    python purview_connect.py --env-file parameters.txt

List all collections:
    python purview_connect.py --list-collections

Search the catalog:
    python purview_connect.py --search "customer data"

Get entity by GUID:
    python purview_connect.py --get-entity xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

JSON output (add to any command):
    python purview_connect.py --list-collections --json

COMMAND-LINE ARGUMENTS
----------------------
--env-file          Path to parameters file (default: parameters.txt)
--list-collections  List all collections in the Purview account
--search <keywords> Search the catalog for the given keywords
--get-entity <guid> Get entity details by GUID
--json              Output results in JSON format

SECURITY CONSIDERATIONS
-----------------------
1. Never commit credentials to version control
2. Use environment variables or Azure Key Vault in production
3. Rotate secrets regularly per your organization's policies
4. Grant service principal only minimum required permissions
5. Review service principal access logs periodically

PROGRAMMATIC USAGE
------------------
    from purview_connect import PurviewConnection

    purview = PurviewConnection(
        purview_name="mypurview",
        tenant_id="xxx",
        client_id="xxx",
        client_secret="xxx"
    )

    if purview.test_connection():
        collections = purview.list_collections()
        results = purview.search_catalog("customer")

===============================================================================
"""

import os
import sys
import argparse
import json
from typing import Optional

try:
    from azure.identity import ClientSecretCredential
    from azure.purview.catalog import PurviewCatalogClient
    from azure.purview.administration.account import PurviewAccountClient
except ImportError as e:
    print("Required packages are missing. Please install them:")
    print("  pip install azure-identity azure-purview-catalog azure-purview-administration")
    sys.exit(1)


class PurviewConnection:
    """A class to manage connections to Microsoft Purview Data Governance."""

    def __init__(
        self,
        purview_name: str,
        tenant_id: str,
        client_id: str,
        client_secret: str,
    ):
        """
        Initialize the Purview connection.

        Args:
            purview_name: Name of the Purview account
            tenant_id: Azure AD tenant ID
            client_id: Service principal client ID
            client_secret: Service principal client secret
        """
        self.purview_name = purview_name
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        
        # Purview endpoints
        self.purview_endpoint = f"https://{purview_name}.purview.azure.com"
        self.catalog_endpoint = f"https://{purview_name}.purview.azure.com"
        self.account_endpoint = f"https://{purview_name}.purview.azure.com"
        
        # Initialize credential and clients
        self._credential = None
        self._catalog_client = None
        self._account_client = None

    @property
    def credential(self) -> ClientSecretCredential:
        """Get or create the Azure credential."""
        if self._credential is None:
            self._credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
        return self._credential

    @property
    def catalog_client(self) -> PurviewCatalogClient:
        """Get or create the Purview Catalog client."""
        if self._catalog_client is None:
            self._catalog_client = PurviewCatalogClient(
                endpoint=self.catalog_endpoint,
                credential=self.credential,
            )
        return self._catalog_client

    @property
    def account_client(self) -> PurviewAccountClient:
        """Get or create the Purview Account client."""
        if self._account_client is None:
            self._account_client = PurviewAccountClient(
                endpoint=self.account_endpoint,
                credential=self.credential,
            )
        return self._account_client

    def test_connection(self) -> bool:
        """
        Test the connection to Purview by getting account information.

        Returns:
            True if connection is successful, False otherwise.
        """
        try:
            account_info = self.account_client.accounts.get_account_properties()
            print("✓ Successfully connected to Purview!")
            print(f"  Account Name: {account_info.get('name', 'N/A')}")
            print(f"  Friendly Name: {account_info.get('properties', {}).get('friendlyName', 'N/A')}")
            print(f"  Endpoint: {self.purview_endpoint}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to Purview: {e}")
            return False

    def get_account_info(self) -> dict:
        """Get Purview account information."""
        return self.account_client.accounts.get_account_properties()

    def list_collections(self) -> list:
        """List all collections in the Purview account."""
        collections = self.account_client.collections.list_collections()
        return list(collections)

    def search_catalog(self, keywords: str, limit: int = 10) -> dict:
        """
        Search the Purview catalog.

        Args:
            keywords: Search keywords
            limit: Maximum number of results to return

        Returns:
            Search results dictionary
        """
        search_body = {
            "keywords": keywords,
            "limit": limit,
        }
        return self.catalog_client.discovery.query(search_request=search_body)

    def get_entity_by_guid(self, guid: str) -> dict:
        """
        Get an entity by its GUID.

        Args:
            guid: The entity GUID

        Returns:
            Entity details dictionary
        """
        return self.catalog_client.entity.get_by_guid(guid=guid)

    def list_glossary_terms(self) -> list:
        """List all glossary terms."""
        glossary = self.catalog_client.glossary.list_glossaries()
        terms = []
        for g in glossary:
            if 'termInfo' in g:
                terms.extend(g['termInfo'].values())
        return terms


def load_parameters_from_file(filepath: str) -> dict:
    """
    Load parameters from a file (key=value format).

    Args:
        filepath: Path to the parameters file

    Returns:
        Dictionary of parameters
    """
    params = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                params[key.strip()] = value.strip()
    return params


def get_config(env_file: Optional[str] = None) -> dict:
    """
    Get configuration from environment variables or parameters file.

    Args:
        env_file: Optional path to parameters file

    Returns:
        Configuration dictionary with purview_name, tenant_id, client_id, client_secret
    """
    config = {}

    # If env file is provided, load it first
    if env_file and os.path.exists(env_file):
        file_params = load_parameters_from_file(env_file)
        
        config['purview_name'] = file_params.get('PURVIEW_NAME')
        config['tenant_id'] = file_params.get('TENANT_ID') or file_params.get('AZURE_TENANT_ID')
        config['client_id'] = file_params.get('CLIENT_ID') or file_params.get('AZURE_CLIENT_ID')
        config['client_secret'] = file_params.get('CLIENT_SECRET') or file_params.get('AZURE_CLIENT_SECRET')

    # Environment variables override file values
    config['purview_name'] = os.environ.get('PURVIEW_NAME', config.get('purview_name'))
    config['tenant_id'] = os.environ.get('AZURE_TENANT_ID') or os.environ.get('TENANT_ID') or config.get('tenant_id')
    config['client_id'] = os.environ.get('AZURE_CLIENT_ID') or os.environ.get('CLIENT_ID') or config.get('client_id')
    config['client_secret'] = os.environ.get('AZURE_CLIENT_SECRET') or os.environ.get('CLIENT_SECRET') or config.get('client_secret')

    return config


def validate_config(config: dict) -> bool:
    """
    Validate that all required configuration is present.

    Args:
        config: Configuration dictionary

    Returns:
        True if valid, False otherwise
    """
    required = ['purview_name', 'tenant_id', 'client_id', 'client_secret']
    missing = [key for key in required if not config.get(key)]
    
    if missing:
        print("Missing required configuration:")
        for key in missing:
            env_name = f"AZURE_{key.upper()}" if key != 'purview_name' else 'PURVIEW_NAME'
            print(f"  - {env_name}")
        print("\nSet these as environment variables or provide a parameters file.")
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Connect to Microsoft Purview Data Governance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python purview_connect.py
  python purview_connect.py --env-file parameters.txt
  python purview_connect.py --list-collections
  python purview_connect.py --search "customer data"
        """
    )
    parser.add_argument(
        '--env-file',
        help='Path to parameters file (key=value format)',
        default='parameters.txt'
    )
    parser.add_argument(
        '--list-collections',
        action='store_true',
        help='List all collections'
    )
    parser.add_argument(
        '--search',
        help='Search the catalog for the given keywords'
    )
    parser.add_argument(
        '--get-entity',
        help='Get entity by GUID'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )

    args = parser.parse_args()

    # Load configuration
    config = get_config(args.env_file)
    
    if not validate_config(config):
        sys.exit(1)

    # Print connection info
    print("=" * 60)
    print("Purview Data Governance Connection")
    print("=" * 60)
    print(f"Purview Account: {config['purview_name']}")
    print(f"Tenant ID: {config['tenant_id']}")
    print(f"Client ID: {config['client_id']}")
    print(f"Client Secret: {'*' * 8}...{config['client_secret'][-4:]}")
    print("=" * 60)
    print()

    # Create connection
    purview = PurviewConnection(
        purview_name=config['purview_name'],
        tenant_id=config['tenant_id'],
        client_id=config['client_id'],
        client_secret=config['client_secret'],
    )

    # Test connection
    if not purview.test_connection():
        sys.exit(1)

    print()

    # Execute requested action
    if args.list_collections:
        print("Collections:")
        print("-" * 40)
        collections = purview.list_collections()
        if args.json:
            print(json.dumps(collections, indent=2))
        else:
            for coll in collections:
                name = coll.get('name', 'N/A')
                friendly = coll.get('friendlyName', name)
                parent = coll.get('parentCollection', {}).get('referenceName', 'root')
                print(f"  - {friendly} ({name}) [parent: {parent}]")

    elif args.search:
        print(f"Search results for: '{args.search}'")
        print("-" * 40)
        results = purview.search_catalog(args.search)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for item in results.get('value', []):
                name = item.get('name', 'N/A')
                qualified_name = item.get('qualifiedName', 'N/A')
                entity_type = item.get('entityType', 'N/A')
                print(f"  - {name}")
                print(f"    Type: {entity_type}")
                print(f"    Qualified Name: {qualified_name}")
                print()

    elif args.get_entity:
        print(f"Entity details for GUID: {args.get_entity}")
        print("-" * 40)
        entity = purview.get_entity_by_guid(args.get_entity)
        if args.json:
            print(json.dumps(entity, indent=2))
        else:
            ent = entity.get('entity', {})
            print(f"  Name: {ent.get('attributes', {}).get('name', 'N/A')}")
            print(f"  Type: {ent.get('typeName', 'N/A')}")
            print(f"  Qualified Name: {ent.get('attributes', {}).get('qualifiedName', 'N/A')}")
            print(f"  GUID: {ent.get('guid', 'N/A')}")

    print()
    print("Connection successful. Ready for further operations.")


if __name__ == '__main__':
    main()
