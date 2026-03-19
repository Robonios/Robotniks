"""
Robotniks Archive Utilities
============================
Shared merge-and-write pattern for fetcher scripts.
Keeps a full historical archive (for co-pilot training) and returns
only the items passing a retention filter for the live JSON output.

No external dependencies — stdlib only.
"""

import json
from pathlib import Path


def load_json(path):
    """Load JSON file, return empty dict if missing or malformed."""
    p = Path(path)
    if p.exists():
        try:
            with open(p) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def archive_and_filter(items, archive_path, key_field, current_filter_fn, data_key):
    """
    Merge new items into archive, return items passing retention filter.

    Args:
        items: list of newly fetched items
        archive_path: path to archive JSON file (grows over time)
        key_field: field to deduplicate on (e.g. 'id', 'url')
        current_filter_fn: function(item) -> bool — True if item belongs in live output
        data_key: JSON key name (e.g. 'items', 'papers', 'filings', 'reports')

    Returns:
        list of items passing current_filter_fn, sorted by date desc
    """
    # Load existing archive
    archive_data = load_json(archive_path)
    archived_items = archive_data.get(data_key, [])

    # Build lookup by key — existing first, new items overwrite
    all_items = {}
    for item in archived_items:
        key = item.get(key_field, "")
        if key:
            all_items[key] = item
    for item in items:
        key = item.get(key_field, "")
        if key:
            all_items[key] = item

    # Sort all items by date descending
    all_list = sorted(all_items.values(), key=lambda x: x.get("date", "") or "0000", reverse=True)

    # Write full archive
    archive_output = {
        "archived_count": len(all_list),
        data_key: all_list,
    }
    Path(archive_path).parent.mkdir(parents=True, exist_ok=True)
    with open(archive_path, "w") as f:
        json.dump(archive_output, f, indent=2)

    # Filter for current/live output
    current = [item for item in all_list if current_filter_fn(item)]
    return current
