from apps.config import AppConfig


def get_test_app_config() -> AppConfig:
    return AppConfig()


class BaseTestCase:
    base_url: str

    def get_url(self) -> str:
        return self.base_url
