from dataclasses import dataclass, field
import environ
import pathlib


# выделяем настройки в отдельный объект, для снижения связанности кода
# так удобнее писать автотесты


@dataclass
class Settings:
    # Объект окружения, из которого мы достаём параметры.
    env: environ.Env = field(default_factory=environ.Env)
    # Путь до .env файла.
    env_path: pathlib.Path = field(default=None)
    # Путь до корня проекта.
    BASE_DIR: pathlib.Path = field(init=False)

    # Настройки проекта
    # URL до redis экстрактора.
    EXTRACTOR_TO_TRANSFORMER_QUERY_HOST: str = field(init=False)
    # URL до redis трансформера.
    TRANSFORMER_TO_LOADER_QUERY_HOST: str = field(init=False)

    def __post_init__(self):
        self.BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
        self.env_path = self.BASE_DIR / ".env" if not self.env_path else self.env_path
        environ.Env.read_env(self.env_file_path.as_posix())
        self.EXTRACTOR_TO_TRANSFORMER_QUERY_HOST: str = self.env.db_url(
            "EXTRACTOR_TO_TRANSFORMER_QUERY_HOST"
        )
        self.TRANSFORMER_TO_LOADER_QUERY_HOST: str = self.env.db_url(
            "TRANSFORMER_TO_LOADER_QUERY_HOST"
        )
