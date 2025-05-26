#!/usr/bin/env python3
# download_pdb.py
# Description: Downloads PDB files from the RCSB PDB database.
# Dependencies: requests (install with: pip install requests)
#
# Usage examples:
# python download_pdb.py --pdb_ids "1EHZ,2ABC"
# python download_pdb.py --pdb_ids "1EHZ,2ABC,INVALIDID" --output_dir "custom_pdb_downloads"
# python download_pdb.py --id_file "pdb_ids.txt"
# python download_pdb.py --id_file "pdb_ids.txt" --output_dir "my_proteins"
#
# Example pdb_ids.txt:
# 1EHZ
# 1XYZ
# 2ABC

import argparse
import os
import requests
import sys # Import sys for exit codes

# Base URL for PDB file downloads from RCSB
RCSB_DOWNLOAD_URL = "https://files.rcsb.org/download/{}.pdb"

def download_pdb_file(pdb_id, output_dir):
    """
    Downloads a single PDB file from RCSB.

    Args:
        pdb_id (str): The PDB ID to download (e.g., "1EHZ").
        output_dir (str): The directory to save the downloaded file.

    Returns:
        bool: True if download was successful, False otherwise.
    """
    pdb_id = pdb_id.upper()
    download_url = RCSB_DOWNLOAD_URL.format(pdb_id)
    
    # Ensure output directory exists
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create directory {output_dir}. {e}", file=sys.stderr)
        return False # Cannot proceed if directory cannot be created

    output_filename = os.path.join(output_dir, f"{pdb_id}.pdb")

    print(f"Attempting to download PDB ID: {pdb_id} from {download_url}...")

    try:
        response = requests.get(download_url, timeout=15) # Increased timeout slightly
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded and saved: {output_filename}")
        return True

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error: PDB ID {pdb_id} not found (404 Error). URL: {download_url}", file=sys.stderr)
        else:
            print(f"Error downloading {pdb_id}: HTTP Error {e.response.status_code} for URL {download_url}", file=sys.stderr)
    except requests.exceptions.ConnectionError:
        print(f"Error downloading {pdb_id}: Connection error. Check your network connection and the URL: {download_url}", file=sys.stderr)
    except requests.exceptions.Timeout:
        print(f"Error downloading {pdb_id}: Request timed out for URL: {download_url}", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {pdb_id}: An unexpected error occurred: {e} for URL: {download_url}", file=sys.stderr)
    except IOError as e:
        print(f"Error saving file {output_filename}: {e}", file=sys.stderr)
    
    return False

def main():
    """
    Main function to parse arguments, create directories, and download PDB files.
    """
    parser = argparse.ArgumentParser(
        description="Download PDB files from RCSB.",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--pdb_ids",
        type=str,
        help="A comma-separated string of PDB IDs (e.g., '1EHZ,1XYZ,2ABC')."
    )
    input_group.add_argument(
        "--id_file",
        type=str,
        help="Path to a file containing PDB IDs, one ID per line."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="pdb_downloads",
        help="The directory to save downloaded PDB files (default: 'pdb_downloads')."
    )

    args = parser.parse_args()

    pdb_ids_to_download = []

    if args.pdb_ids:
        pdb_ids_to_download = [pid.strip().upper() for pid in args.pdb_ids.split(',') if pid.strip()]
    elif args.id_file:
        try:
            with open(args.id_file, 'r') as f:
                pdb_ids_to_download = [line.strip().upper() for line in f if line.strip()]
            if not pdb_ids_to_download:
                print(f"Info: The file {args.id_file} is empty or contains no valid PDB IDs.", file=sys.stdout)
        except FileNotFoundError:
            print(f"Error: ID file not found: {args.id_file}", file=sys.stderr)
            sys.exit(1) # Exit with error
        except IOError as e:
            print(f"Error reading ID file {args.id_file}: {e}", file=sys.stderr)
            sys.exit(1) # Exit with error
    
    # This else is technically not needed due to mutually_exclusive_group(required=True)
    # but kept for logical completeness, though argparse handles the missing input.
    # else:
    #     parser.print_help(sys.stderr) # Print help to stderr
    #     print("\nError: You must provide PDB IDs via --pdb_ids or --id_file.", file=sys.stderr)
    #     sys.exit(1)


    if not pdb_ids_to_download:
        print("No PDB IDs to download.", file=sys.stdout)
        sys.exit(0) # Exit gracefully

    # Output directory creation is now handled by download_pdb_file, 
    # but we can pre-create it here if we want a message specific to main.
    # For consistency, let download_pdb_file handle it.
    # os.makedirs(args.output_dir, exist_ok=True)
    # print(f"Ensuring output directory exists: {args.output_dir}")


    successful_downloads = 0
    total_ids = len(pdb_ids_to_download)
    failed_ids = []

    print(f"\nStarting PDB file downloads to directory: {args.output_dir}")
    for pdb_id in pdb_ids_to_download:
        if download_pdb_file(pdb_id, args.output_dir):
            successful_downloads += 1
        else:
            failed_ids.append(pdb_id)
        print("-" * 30) # Separator

    print(f"\nSummary: {successful_downloads} out of {total_ids} files downloaded successfully.")
    if failed_ids:
        print(f"Failed to download the following PDB IDs: {', '.join(failed_ids)}", file=sys.stderr)
        sys.exit(1) # Exit with error code if some downloads failed
    
    sys.exit(0) # All successful or no IDs to download initially

if __name__ == "__main__":
    main()
