import httpx
import pytest
from pytest_mock import MockerFixture

from lisum_bot.exceptions import LisumError
from lisum_bot.lisum import dialog_request, reaction_request


@pytest.mark.asyncio
async def test_dialog_request(mocker: MockerFixture):
    mock_response = httpx.Response(200, content="Mocked Response")
    mocker.patch(
        "httpx.AsyncClient.patch",
        return_value=mock_response,
        side_effect=Exception("mocked error"),
    )
    with pytest.raises(LisumError):
        await reaction_request(id=123, reaction="Smiling fase")
