from src.apps.auth.enums import Role, Scope

# Each endpoint or feature can define allowed roles and scopes
SEARCH_POLICY = {
    "roles": [Role.VIEWER, Role.EDITOR, Role.ADMIN],
    "scopes": [Scope.DOCUMENT_PREVIEW],
}

PREVIEW_POLICY = {
    "roles": [Role.VIEWER, Role.EDITOR, Role.ADMIN],
    "scopes": [Scope.DOCUMENT_PREVIEW],
}

DOWNLOAD_POLICY = {
    "roles": [Role.EDITOR, Role.ADMIN],
    "scopes": [Scope.DOCUMENT_DOWNLOAD],
}

MANAGE_POLICY = {
    "roles": [Role.ADMIN],
    "scopes": [Scope.DOCUMENT_MANAGE],
}
