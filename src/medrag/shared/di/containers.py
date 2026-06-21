from dependency_injector import containers, providers

from medrag.shared.config.settings import settings


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection container.
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "medrag.api",
        ]
    )

    settings = providers.Object(settings)
