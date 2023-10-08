def path_to_uploaded_img(instance, filename):
    """Creates path to uploaded image."""
    return f"{instance.user.id}/images/{instance.id}/{filename}"
