def path_to_uploaded_img():
    """Creates path to uploaded image."""
    return f"{instance.user.id}/images/{instance.id}/{filename}"
