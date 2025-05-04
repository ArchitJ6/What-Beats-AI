import pytest
import httpx
import asyncio
import json
import websockets
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables from e nv file
BASE_URL = os.getenv("VITE_API_URL")
WS_URL = os.getenv("VITE_WS_BASE_URL")

@pytest.mark.asyncio
async def test_duplicate_guess_returns_game_over():
    # Step 1: Connect to WebSocket to get session_id
    async with websockets.connect(WS_URL) as ws:
        # Wait for the initial message with session_id
        message = await ws.recv()
        data = json.loads(message)
        session_id = data["session_id"]
        assert session_id is not None

    # Step 2: Submit a valid guess
    guess1_payload = {
        "seed": "Rock",
        "guess": "Paper",
        "session_id": session_id,
        "persona": "serious"
    }
    async with httpx.AsyncClient() as client:
        response1 = await client.post(f"{BASE_URL}/guess", json=guess1_payload)
        assert response1.status_code == 200
        assert response1.json()["status"] == "success"

        # Step 3: Submit the same guess again
        response2 = await client.post(f"{BASE_URL}/guess", json=guess1_payload)
        assert response2.status_code == 200
        assert response2.json()["status"] == "game_over"
        assert "already used" in response2.json()["message"]

@pytest.mark.asyncio
async def test_game_flow_with_websocket():
    # 1. Connect to WebSocket and receive session_id
    async with websockets.connect(WS_URL) as ws:
        msg = await ws.recv()
        data = json.loads(msg)
        assert "session_id" in data
        session_id = data["session_id"]

        # 2. Call /history before playing
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{BASE_URL}/history", params={"session_id": session_id})
            assert res.status_code == 200
            assert res.json()["history"] == []

            # 3. Make a guess
            guess_payload = {
                "session_id": session_id,
                "seed": "fire",
                "guess": "water",
                "persona": "serious"
            }
            guess_res = await client.post(f"{BASE_URL}/guess", json=guess_payload)
            assert guess_res.status_code == 200
            assert guess_res.json()["status"] in ["success", "fail", "game_over"]

            # 4. Call /reset
            reset_res = await client.post(f"{BASE_URL}/reset?session_id={session_id}")
            assert reset_res.status_code == 200
            assert reset_res.json()["message"] == "Game reset."

            # 5. Confirm reset
            res2 = await client.get(f"{BASE_URL}/history", params={"session_id": session_id})
            assert res2.status_code == 200
            assert res2.json()["history"] == []

        await asyncio.sleep(1)  # Let one more message come via websocket