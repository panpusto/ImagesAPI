"""
Three built-in tiers:
Basic, Premium and Enterprise.
Created after database migration.
"""

DEFAULT_TIERS = {
    "Basic": dict(
        thumbnail_size=dict(height=200),
        is_expiration_link=False,
        is_original_file=False
    ),
    "Premium": dict(
        thumbnail_size=dict(height=400),
        is_expiration_link=False,
        is_original_file=True
    ),
    "Enterprise": dict(
        is_expiration_link=True,
        is_original_file=True
    )
}
