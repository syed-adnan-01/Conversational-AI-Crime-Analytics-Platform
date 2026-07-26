"""HTTP client for Zoho Catalyst QuickML RAG answer endpoint."""

from __future__ import annotations

import time
from typing import Any

import httpx
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.ai.quickml.quickml_config import QuickMLConfig, quickml_config
from app.ai.quickml.quickml_models import QuickMLRetrievalRequest, QuickMLRetrievalResult


class QuickMLClient:
    def __init__(
        self,
        config: QuickMLConfig | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.config = config or quickml_config
        self._client = client or httpx.Client(timeout=self.config.QUICKML_TIMEOUT)
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def answer(self, query: str, documents: list[str]) -> QuickMLRetrievalResult:
        if not self.config.is_configured:
            raise RuntimeError("QuickML is not fully configured")

        request_payload = QuickMLRetrievalRequest(query=query, documents=documents)
        url = (
            f"https://console.catalyst.zoho.in/quickml/v1/project/"
            f"{self.config.CATALYST_PROJECT_ID}/rag/answer"
        )
        headers = {
            "Authorization": f"Zoho-oauthtoken {self.config.ZOHO_ACCESS_TOKEN}",
            "CATALYST-ORG": self.config.CATALYST_ORG_ID,
        }

        started = time.perf_counter()
        response: httpx.Response | None = None
        for attempt in Retrying(
            stop=stop_after_attempt(self.config.QUICKML_MAX_RETRIES),
            wait=wait_exponential(multiplier=0.2, min=0.2, max=2.0),
            retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError)),
            reraise=True,
        ):
            with attempt:
                response = self._client.post(url, headers=headers, json=request_payload.model_dump())
                response.raise_for_status()

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        payload = response.json() if response is not None else {}
        return self._parse_payload(request_payload, payload, elapsed_ms)

    def _parse_payload(
        self,
        request_payload: QuickMLRetrievalRequest,
        payload: Any,
        elapsed_ms: int,
    ) -> QuickMLRetrievalResult:
        if not isinstance(payload, dict):
            payload = {}

        answer = (
            payload.get("answer")
            or payload.get("response")
            or payload.get("content")
            or payload.get("text")
            or payload.get("message")
            or ""
        )
        citations = self._extract_citations(payload)
        confidence = self._extract_confidence(payload)
        metadata = {k: v for k, v in payload.items() if k not in {"answer", "response", "content", "text", "message"}}
        return QuickMLRetrievalResult(
            query=request_payload.query,
            answer=str(answer),
            citations=citations,
            confidence=confidence,
            latency_ms=elapsed_ms,
            documents=request_payload.documents,
            metadata=metadata,
        )

    @staticmethod
    def _extract_citations(payload: dict[str, Any]) -> list[str]:
        raw = payload.get("citations") or payload.get("sources") or payload.get("references") or []
        if isinstance(raw, list):
            citations: list[str] = []
            for item in raw:
                if isinstance(item, str):
                    citations.append(item)
                elif isinstance(item, dict):
                    value = item.get("id") or item.get("doc_id") or item.get("citation") or item.get("reference")
                    if value:
                        citations.append(str(value))
            return citations
        if isinstance(raw, str) and raw.strip():
            return [raw.strip()]
        return []

    @staticmethod
    def _extract_confidence(payload: dict[str, Any]) -> float:
        for key in ("confidence", "score", "relevance", "similarity"):
            value = payload.get(key)
            if isinstance(value, (int, float)):
                return float(value)
        return 0.0