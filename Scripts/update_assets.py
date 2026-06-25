import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


class PurviewClient:
    """Client for authenticating and interacting with Azure Purview Data Governance."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        purview_name: str
    ):
        """
        Initialize the Purview client.

        Args:
            client_id: The Azure AD application (client) ID
            client_secret: The client secret for the application
            tenant_id: The Azure AD tenant ID
            purview_name: The name of the Purview account
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.purview_name = purview_name
        self.access_token: Optional[str] = None
        
        # Azure Purview endpoints
        self.purview_endpoint = f"https://{purview_name}.purview.azure.com"
        self.token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        
        # Scope for Azure Purview
        self.scope = "https://purview.azure.net/.default"

    def login(self) -> bool:
        """
        Authenticate to Azure Purview using client credentials.

        Returns:
            bool: True if authentication was successful, False otherwise
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(
                self.token_url,
                data=payload,
                headers=headers
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            
            if self.access_token:
                print(f"Successfully authenticated to Purview account: {self.purview_name}")
                return True
            else:
                print("Authentication failed: No access token received")
                return False
                
        except requests.exceptions.HTTPError as e:
            print(f"Authentication failed with HTTP error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed with error: {e}")
            return False

    def get_headers(self) -> dict:
        """
        Get the authorization headers for API requests.

        Returns:
            dict: Headers including the Bearer token

        Raises:
            ValueError: If not authenticated (no access token)
        """
        if not self.access_token:
            raise ValueError("Not authenticated. Call login() first.")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def is_authenticated(self) -> bool:
        """
        Check if the client is authenticated.

        Returns:
            bool: True if authenticated, False otherwise
        """
        return self.access_token is not None

    def search_assets(self, keyword: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search for assets in Purview using a keyword.

        Args:
            keyword: The search keyword
            limit: Maximum number of results to return

        Returns:
            List of matching asset dictionaries
        """
        search_url = f"{self.purview_endpoint}/catalog/api/search/query?api-version=2022-08-01-preview"
        
        payload = {
            "keywords": keyword,
            "limit": limit
        }

        try:
            response = requests.post(
                search_url,
                json=payload,
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            return result.get("value", [])
        except requests.exceptions.RequestException as e:
            print(f"Search failed: {e}")
            return []

    def find_column_asset(
        self,
        table_name: str,
        column_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find a column asset in Purview by table name and column name.

        Args:
            table_name: The name of the table
            column_name: The name of the column

        Returns:
            The matching column asset, or None if not found
        """
        search_url = f"{self.purview_endpoint}/catalog/api/search/query?api-version=2022-08-01-preview"
        
        # Search for the column by name, then filter by table
        payload = {
            "keywords": column_name,
            "filter": {
                "and": [
                    {
                        "entityType": "column"
                    }
                ]
            },
            "limit": 100
        }

        try:
            response = requests.post(
                search_url,
                json=payload,
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            assets = result.get("value", [])

            # Filter results to find exact match for table and column
            for asset in assets:
                asset_name = asset.get("name", "")
                qualified_name = asset.get("qualifiedName", "")
                
                # Check if column name matches and table name is in the qualified name
                if (asset_name.lower() == column_name.lower() and
                    table_name.lower() in qualified_name.lower()):
                    return asset

            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Search failed for {table_name}.{column_name}: {e}")
            return None

    def get_asset_by_guid(self, guid: str) -> Optional[Dict[str, Any]]:
        """
        Get an asset by its GUID.

        Args:
            guid: The unique identifier of the asset

        Returns:
            The asset details, or None if not found
        """
        url = f"{self.purview_endpoint}/catalog/api/atlas/v2/entity/guid/{guid}"

        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get asset {guid}: {e}")
            return None

    def assign_glossary_term_to_asset(
        self,
        asset_guid: str,
        glossary_term_name: str
    ) -> bool:
        """
        Assign a glossary term to an asset by GUID.

        Args:
            asset_guid: The GUID of the asset to update
            glossary_term_name: The name of the glossary term to assign

        Returns:
            bool: True if successful, False otherwise
        """
        # First, search for the glossary term to get its GUID
        term_guid = self._get_glossary_term_guid(glossary_term_name)
        if not term_guid:
            print(f"Glossary term '{glossary_term_name}' not found")
            return False

        # Assign the term to the asset
        url = f"{self.purview_endpoint}/catalog/api/atlas/v2/glossary/terms/{term_guid}/assignedEntities"
        
        payload = [
            {
                "guid": asset_guid
            }
        ]

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.get_headers()
            )
            response.raise_for_status()
            print(f"Successfully assigned glossary term '{glossary_term_name}' to asset {asset_guid}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to assign glossary term: {e}")
            return False

    def _get_glossary_term_guid(self, term_name: str) -> Optional[str]:
        """
        Get the GUID of a glossary term by name.

        Args:
            term_name: The name of the glossary term

        Returns:
            The GUID of the term, or None if not found
        """
        search_url = f"{self.purview_endpoint}/catalog/api/search/query?api-version=2022-08-01-preview"
        
        payload = {
            "keywords": term_name,
            "filter": {
                "and": [
                    {
                        "entityType": "AtlasGlossaryTerm"
                    }
                ]
            },
            "limit": 100
        }

        try:
            response = requests.post(
                search_url,
                json=payload,
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            terms = result.get("value", [])

            # Find exact match for term name
            for term in terms:
                if term.get("name", "").lower() == term_name.lower():
                    return term.get("id")

            return None
        except requests.exceptions.RequestException as e:
            print(f"Failed to search for glossary term: {e}")
            return None


def process_asset_mappings(
    client: PurviewClient,
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Process a DataFrame of asset mappings and find corresponding Purview assets.

    Args:
        client: An authenticated PurviewClient
        df: DataFrame with columns: table_name, column_name, glossary_term

    Returns:
        DataFrame with additional columns for asset information:
        - asset_guid: The GUID of the found asset (or None)
        - asset_qualified_name: The qualified name of the asset (or None)
        - asset_found: Boolean indicating if asset was found
    """
    if not client.is_authenticated():
        raise ValueError("Client is not authenticated. Call login() first.")

    results = []
    total_rows = len(df)

    print(f"Processing {total_rows} rows...")

    for idx, (index, row) in enumerate(df.iterrows()):
        table_name = row["table_name"]
        column_name = row["column_name"]
        glossary_term = row["glossary_term"]

        print(f"[{idx + 1}/{total_rows}] Searching for {table_name}.{column_name}...")

        asset = client.find_column_asset(table_name, column_name)

        if asset:
            results.append({
                "table_name": table_name,
                "column_name": column_name,
                "glossary_term": glossary_term,
                "asset_guid": asset.get("id"),
                "asset_qualified_name": asset.get("qualifiedName"),
                "asset_found": True
            })
            print(f"  Found: {asset.get('qualifiedName')}")
        else:
            results.append({
                "table_name": table_name,
                "column_name": column_name,
                "glossary_term": glossary_term,
                "asset_guid": None,
                "asset_qualified_name": None,
                "asset_found": False
            })
            print(f"  Not found")

    result_df = pd.DataFrame(results)
    
    found_count = result_df["asset_found"].sum()
    print(f"\nProcessing complete. Found {found_count}/{total_rows} assets.")
    
    return result_df


@dataclass
class SearchResults:
    """Container for asset search results with separate DataFrames."""
    
    all_results: pd.DataFrame
    """DataFrame containing all search results"""
    
    found_assets: pd.DataFrame
    """DataFrame containing only assets that were found in Purview"""
    
    not_found_assets: pd.DataFrame
    """DataFrame containing only assets that were not found in Purview"""
    
    @property
    def found_count(self) -> int:
        """Number of assets found."""
        return len(self.found_assets)
    
    @property
    def not_found_count(self) -> int:
        """Number of assets not found."""
        return len(self.not_found_assets)
    
    @property
    def total_count(self) -> int:
        """Total number of assets processed."""
        return len(self.all_results)
    
    def summary(self) -> str:
        """Return a summary of the search results."""
        return (
            f"Search Results Summary:\n"
            f"  Total processed: {self.total_count}\n"
            f"  Found: {self.found_count}\n"
            f"  Not found: {self.not_found_count}"
        )


def search_and_store_assets(
    client: PurviewClient,
    df: pd.DataFrame
) -> SearchResults:
    """
    Search for assets in Purview and store results in separate DataFrames.

    Args:
        client: An authenticated PurviewClient
        df: DataFrame with columns: table_name, column_name, glossary_term

    Returns:
        SearchResults: Object containing three DataFrames:
            - all_results: All processed rows with asset information
            - found_assets: Only rows where assets were found
            - not_found_assets: Only rows where assets were not found
    """
    # Process all asset mappings
    all_results_df = process_asset_mappings(client, df)
    
    # Split into found and not found DataFrames
    found_df = all_results_df[all_results_df["asset_found"] == True].copy()
    not_found_df = all_results_df[all_results_df["asset_found"] == False].copy()
    
    # Reset indices for cleaner DataFrames
    found_df.reset_index(drop=True, inplace=True)
    not_found_df.reset_index(drop=True, inplace=True)
    
    results = SearchResults(
        all_results=all_results_df,
        found_assets=found_df,
        not_found_assets=not_found_df
    )
    
    print(results.summary())
    
    return results


def update_glossary_terms_for_assets(
    client: PurviewClient,
    found_assets_df: pd.DataFrame,
    execute_update: bool = False
) -> pd.DataFrame:
    """
    Loop through found assets and update glossary terms in Purview.

    Args:
        client: An authenticated PurviewClient
        found_assets_df: DataFrame with found assets (from SearchResults.found_assets)
        execute_update: Set to True to actually perform updates (default: False for dry run)

    Returns:
        DataFrame with update status for each row
    """
    if not client.is_authenticated():
        raise ValueError("Client is not authenticated. Call login() first.")

    update_results = []
    total_rows = len(found_assets_df)

    print(f"Processing {total_rows} assets for glossary term updates...")
    print(f"Execute mode: {'LIVE' if execute_update else 'DRY RUN'}")

    for idx, (_, row) in enumerate(found_assets_df.iterrows()):
        table_name = row["table_name"]
        column_name = row["column_name"]
        glossary_term = row["glossary_term"]
        asset_guid = row["asset_guid"]
        asset_qualified_name = row["asset_qualified_name"]

        print(f"\n[{idx + 1}/{total_rows}] Processing {table_name}.{column_name}")
        print(f"  Asset GUID: {asset_guid}")
        print(f"  Glossary term to assign: {glossary_term}")

        update_status = "skipped"
        error_message = None

        # Condition placeholder: change 1 == 2 to 1 == 1 (or True) to enable updates
        if 1 == 2:  # Always False - change to True or 1 == 1 to enable
            if execute_update:
                try:
                    success = client.assign_glossary_term_to_asset(
                        asset_guid=asset_guid,
                        glossary_term_name=glossary_term
                    )
                    update_status = "success" if success else "failed"
                except Exception as e:
                    update_status = "error"
                    error_message = str(e)
                    print(f"  Error: {e}")
            else:
                update_status = "dry_run"
                print(f"  [DRY RUN] Would assign glossary term '{glossary_term}' to asset")
        else:
            print(f"  Skipped (condition not met)")

        update_results.append({
            "table_name": table_name,
            "column_name": column_name,
            "glossary_term": glossary_term,
            "asset_guid": asset_guid,
            "asset_qualified_name": asset_qualified_name,
            "update_status": update_status,
            "error_message": error_message
        })

    result_df = pd.DataFrame(update_results)
    
    # Print summary
    status_counts = result_df["update_status"].value_counts()
    print(f"\n--- Update Summary ---")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")

    return result_df


def load_csv_file(csv_file: str) -> pd.DataFrame:
    """
    Load a CSV file with asset mapping data into a DataFrame.

    The CSV file must have a header with the following columns:
    - table_name: The name of the table
    - column_name: The name of the column
    - glossary_term: The glossary term to associate

    Args:
        csv_file: Path to the CSV file

    Returns:
        pd.DataFrame: DataFrame containing the CSV data

    Raises:
        FileNotFoundError: If the CSV file does not exist
        ValueError: If required columns are missing
    """
    required_columns = ["table_name", "column_name", "glossary_term"]
    
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
    # Validate that all required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"CSV file is missing required columns: {missing_columns}. "
            f"Expected columns: {required_columns}"
        )
    
    print(f"Successfully loaded {len(df)} rows from {csv_file}")
    return df


def login_to_purview(
    client_id: str,
    client_secret: str,
    tenant_id: str,
    purview_name: str
) -> Optional[PurviewClient]:
    """
    Convenience function to create a PurviewClient and authenticate.

    Args:
        client_id: The Azure AD application (client) ID
        client_secret: The client secret for the application
        tenant_id: The Azure AD tenant ID
        purview_name: The name of the Purview account

    Returns:
        PurviewClient: An authenticated client, or None if authentication failed
    """
    client = PurviewClient(
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id,
        purview_name=purview_name
    )
    
    if client.login():
        return client
    return None


# Example usage
if __name__ == "__main__":
    # Replace these with your actual values or use environment variables
    import os
    
    CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "your-client-id")
    CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "your-client-secret")
    TENANT_ID = os.environ.get("AZURE_TENANT_ID", "your-tenant-id")
    PURVIEW_NAME = os.environ.get("PURVIEW_NAME", "your-purview-account-name")

    # Login to Purview
    client = login_to_purview(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        tenant_id=TENANT_ID,
        purview_name=PURVIEW_NAME
    )
    
    if client:
        print("Ready to interact with Purview APIs")
        print("")
        print("Client_id =", CLIENT_ID)
        print("Client_Secret =",CLIENT_SECRET)
        print("Tenant_id =", TENANT_ID)
        print("Purview_name= ", PURVIEW_NAME)

        # Use client.get_headers() for subsequent API calls
    else:
        print("Failed to authenticate")
