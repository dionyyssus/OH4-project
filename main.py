import asyncio

from src.services.ai_service import AIService
from src.core.matcher import Matcher, Candidate
from src.concurrency.pipeline import Pipeline, ItemInput


async def main():
    # 1. Set up the shared service, pipeline, and matcher
    ai_service = AIService()
    pipeline = Pipeline(ai_service)
    matcher = Matcher(ai_service=ai_service)

    # 2. Sample items to process (image path + free-text description)
    items = [
        ItemInput(item_id="item-1", image_path="path/to/image1.jpg", user_text="lost near the library"),
        ItemInput(item_id="item-2", image_path="path/to/image2.jpg", user_text="black leather wallet found near the library"),
    ]

    print("--- Running pipeline ---")
    processed_items = await pipeline.process_batch(items)
    for result in processed_items:
        print(f"{result.item_id}: ok={result.ok}, error={result.error}")

    # 3. Build a candidate pool from the successfully processed items and match the first against the rest
    candidates = [r.candidate for r in processed_items if r.ok and r.candidate is not None]
    if len(candidates) < 2:
        print("Not enough successfully processed items to run a match.")
        return

    target = candidates[0]
    pool = candidates[1:]

    matches = matcher.match_with_ids(target, pool, k=1)
    print("--- Match results ---")
    print(matches)


if __name__ == "__main__":
    asyncio.run(main())