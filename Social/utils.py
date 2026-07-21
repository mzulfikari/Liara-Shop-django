from urllib.parse import urlencode


def build_utm_url(
    base_url, source, medium=None, campaign=None, content=None, term=None
):
    params = {"utm_source": source, "utm_medium": medium, "utm_campaign": campaign}
    if content:
        params["utm_content"] = content
    if term:
        params["utm_term"] = term
    return f"{base_url}?{urlencode(params)}"


def generate_utm_link(
    base_url, source, medium=None, campaign=None, content=None, term=None
):
    """
    Function to make links utm
    """

    return build_utm_url(
        base_url=base_url,
        source=source,
        medium=medium,
        campaign=campaign,
        content=content,
        term=term,
    )
