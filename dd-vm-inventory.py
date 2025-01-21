#!/usr/local/bin/python3.10

import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2 import ApiException

def initialize_datadog_client():
    """Initialize and return an authenticated DataDog API client."""
    try:
        # Get API credentials from environment variables
        api_key = os.getenv('DD_API_KEY')
        app_key = os.getenv('DD_APP_KEY')

        if not api_key or not app_key:
            raise ValueError("DataDog API_KEY and APP_KEY must be set as environment variables")

        # Configure the client
        configuration = Configuration(
            api_key={
                'apiKeyAuth': api_key,
                'appKeyAuth': app_key
            }
        )
        
        # Initialize API client
        return ApiClient(configuration)

    except ApiException as e:
        print(f"Error initializing DataDog client: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise

def get_recent_vms(api_client):
    """Fetch virtual machines that have reported to DataDog in the last 24 hours.
    
    Args:
        api_client: Authenticated DataDog API client
        
    Returns:
        list: List of VM hosts that have reported in last 24 hours
    """
    from datadog_api_client.v2.api.hosts_api import HostsApi
    from datetime import datetime, timedelta
    
    try:
        # Initialize the Hosts API client
        hosts_api = HostsApi(api_client)
        
        # Calculate timestamp for 24 hours ago
        from_time = datetime.now() - timedelta(hours=24)
        
        # Get list of all hosts
        response = hosts_api.list_hosts(
            filter=f"last_reported_at:>{from_time.isoformat()}"
        )
        
        # Extract VM data from response
        vm_hosts = []
        for host in response.data:
            if host.attributes.source in ["aws", "azure", "gcp"]:  # Filter for cloud VMs only
                vm_hosts.append({
                    'name': host.attributes.name,
                    'id': host.id,
                    'last_reported': host.attributes.last_reported_at,
                    'platform': host.attributes.platform,
                    'os': host.attributes.os.name if host.attributes.os else 'Unknown'
                })
                
        return vm_hosts
        
    except ApiException as e:
        print(f"DataDog API error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error fetching VM data: {str(e)}")
        raise

def output_vm_data_as_csv(vm_hosts):
    """Output VM data as CSV to stdout.
    
    Args:
        vm_hosts: List of VM host dictionaries containing platform, id, name and last_reported
    """
    import csv
    import sys
    
    try:
        # Create CSV writer for stdout
        writer = csv.writer(sys.stdout)
        
        # Write header row
        writer.writerow(['platform', 'id', 'name', 'last_reported'])
        
        # Write data rows
        for vm in vm_hosts:
            writer.writerow([
                vm.get('platform', 'NA'),
                vm.get('id', 'NA'),
                vm.get('name', 'NA'), 
                vm.get('last_reported', 'NA'),
                vm.get('os', 'NA')
            ])
            
    except Exception as e:
        print(f"Error writing CSV data: {str(e)}", file=sys.stderr)
        raise

def main():
    """Main function to run the script."""
    
    try:
        api_client = initialize_datadog_client()
        print("Successfully authenticated with DataDog API")   
    except Exception as e:
        print(f"Failed to initialize DataDog client: {str(e)}")
        exit(1)

    try:
        vm_hosts = get_recent_vms(api_client)
        if not vm_hosts:
            print("No VM hosts found in the last 24 hours")
            exit(0)
        output_vm_data_as_csv(vm_hosts)
    except Exception as e:
        print(f"Failed to get VM data: {str(e)}")
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
