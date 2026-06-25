from typing import cast

from fastapi import Request

from medrag.shared.di.containers import Container


def get_container(
    request: Request,
) -> Container:
    """Return application container."""

    return cast(
        Container,
        request.app.state.container,
    )
