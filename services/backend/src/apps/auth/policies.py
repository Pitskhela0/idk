from src.apps.auth.enums import DrawingLocatorGroup

# Groups that are permitted to certain actions

SEARCH_POLICY = {
    "groups": [DrawingLocatorGroup.VIEWER, DrawingLocatorGroup.EDITOR]
}

PREVIEW_POLICY = {
    "groups": [DrawingLocatorGroup.VIEWER, DrawingLocatorGroup.EDITOR]
}

DOWNLOAD_POLICY = {
    "groups": [DrawingLocatorGroup.EDITOR]
}

EMAIL_POLICY = {
    "groups": [DrawingLocatorGroup.EDITOR]
}
