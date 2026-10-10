"""A file whose synthesis fails must not be published (no state saved, no go-service call)."""

import base64
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app import api, llm

EVENT = {
    "data": {
        "fileId": "f1",
        "fileName": "adr.md",
        "mimeType": "text/markdown",
        "content": base64.b64encode(b"# ADR").decode(),
    }
}


@pytest.fixture
def pipeline(monkeypatch):
    mocks = {
        "save_state_to_dapr": MagicMock(),
        "call_go_service": AsyncMock(return_value={"result": "ok"}),
        "send_notification": MagicMock(),
    }
    for name, mock in mocks.items():
        monkeypatch.setattr(api, name, mock)
    monkeypatch.setattr(api.asyncio, "sleep", AsyncMock())
    return mocks


def test_synthesis_error_drops_message_without_publishing(pipeline, monkeypatch):
    def fail(prompt):
        raise llm.SynthesisError("429 RESOURCE_EXHAUSTED")

    monkeypatch.setattr(api, "generate_text_with_gemini", fail)
    response = TestClient(api.app).post("/files", json=EVENT)

    assert response.status_code == 200
    assert response.json() == {"status": "DROP"}
    pipeline["save_state_to_dapr"].assert_not_called()
    pipeline["call_go_service"].assert_not_called()
    message = pipeline["send_notification"].call_args.kwargs["data"]["message"]
    assert "not published" in message


def test_notification_failure_still_drops(pipeline, monkeypatch):
    monkeypatch.setattr(
        api, "generate_text_with_gemini", MagicMock(side_effect=llm.SynthesisError("empty"))
    )
    pipeline["send_notification"].side_effect = RuntimeError("pusher down")
    response = TestClient(api.app).post("/files", json=EVENT)
    assert response.json() == {"status": "DROP"}


def test_successful_synthesis_is_published(pipeline, monkeypatch):
    monkeypatch.setattr(api, "generate_text_with_gemini", lambda prompt: "Analysis")
    response = TestClient(api.app).post("/files", json=EVENT)

    assert response.status_code == 200
    pipeline["save_state_to_dapr"].assert_called_once_with(
        "f1", {"content": "# ADR", "synthesis": "Analysis"}
    )
    pipeline["call_go_service"].assert_awaited_once_with("f1")


def test_llm_raises_instead_of_returning_error_text(monkeypatch):
    monkeypatch.setattr(llm.embeddings, "embed_query", MagicMock(side_effect=RuntimeError("429")))
    with pytest.raises(llm.SynthesisError, match="429"):
        llm.generate_text_with_gemini("prompt")


def test_llm_empty_response_raises(monkeypatch):
    monkeypatch.setattr(llm.embeddings, "embed_query", MagicMock(return_value=[0.1]))
    monkeypatch.setattr(llm.container, "query_items", MagicMock(return_value=[]))
    chat = MagicMock()
    chat.return_value.invoke.return_value = MagicMock(content="")
    monkeypatch.setattr(llm, "ChatGoogleGenerativeAI", chat)
    with pytest.raises(llm.SynthesisError, match="empty"):
        llm.generate_text_with_gemini("prompt")
