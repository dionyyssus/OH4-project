from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch
import numpy as np
import pytest

from ai.schemas import ItemDescription, MatchResult
from src.core.matcher import Candidate, Matcher, build_candidate_pool
from src.concurrency.pipeline import ItemInput, Pipeline, ProcessedItem
from src.services.ai_service import AIService


@pytest.fixture
def pydantic_description():
    return ItemDescription(
        object_class="umbrella",
        colors=["black"],
        brand="Samsonite",
    )
    


@pytest.fixture
def mock_ai_module():

    with patch("src.services.ai_service.ai") as mock_ai:
        yield mock_ai


def test_ai_service_describe_and_embed(mock_ai_module, pydantic_description):
    mock_ai_module.describe_item.return_value = pydantic_description
    mock_ai_module.embed.return_value = np.array([0.1, 0.2, 0.3])

    service = AIService()
    desc, vector = service.describe_and_embed("path/to/img.jpg", "test text")

    assert desc.object_class == "umbrella"
    assert np.allclose(vector, [0.1, 0.2, 0.3])
    mock_ai_module.describe_item.assert_called_once_with("path/to/img.jpg", "test text")
    mock_ai_module.embed.assert_called_once()


def test_matcher_logic(pydantic_description):
    query = Candidate(
        item_id="q1",
        embedding=np.array([1.0, 0.0, 0.0]),
        description=pydantic_description,
    )
    pool = [
        Candidate(
            item_id="f1",
            embedding=np.array([0.9, 0.1, 0.0]),
            description=pydantic_description,
        )
    ]

    with patch("src.core.matcher.top_k") as mock_top_k, \
         patch("src.core.matcher.cosine") as mock_cosine:
        
        mock_top_k.return_value = [MatchResult(candidate_id=0, score=0.95, reason="")]
        mock_cosine.return_value = 0.95

        matcher = Matcher()
        results = matcher.match(query, pool, k=1)

        assert len(results) == 1
        assert results[0].score == 0.95
        assert "object: umbrella" in results[0].reason


@pytest.mark.asyncio
async def test_pipeline_batch_processing(mock_ai_module, pydantic_description):
    mock_ai_module.describe_item.return_value = pydantic_description
    mock_ai_module.embed.return_value = np.array([0.5, 0.5, 0.5])

    ai_service = AIService()
    pipeline = Pipeline(ai_service=ai_service, max_concurrency=2)

    inputs = [
        ItemInput(item_id="item-1", image_path="img1.jpg", user_text="lost umbrella"),
        ItemInput(item_id="item-2", image_path="img2.jpg", user_text="lost bag"),
    ]

    results = await pipeline.process_batch(inputs)

    assert len(results) == 2
    assert all(r.ok for r in results)
    assert results[0].item_id == "item-1"
    assert results[1].candidate is not None