from fastapi import APIRouter, Request, HTTPException
from backend.core.ai_client import check_if_beats
from backend.core.cache import get_cached_verdict, set_cached_verdict
from backend.core.game_logic import GameSession
from backend.core.moderation import is_clean
from backend.db.models import GlobalGuessCount
from backend.db.session import AsyncSessionLocal
from sqlalchemy import select
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from sqlalchemy.exc import IntegrityError
import asyncio
from collections import defaultdict

router = APIRouter()
sessions = {}

@router.post("/guess")
async def guess_word(request: Request):
    body = await request.json()
    seed = body.get("seed")
    guess = body.get("guess")
    session_id = body.get("session_id")
    persona = body.get("persona", "serious")

    if not is_clean(guess):
        raise HTTPException(status_code=400, detail="Inappropriate content.")

    # session = sessions.setdefault(session_id, GameSession())
    session = sessions.get(session_id, None)
    if session is None:
        # Try to refresh the page to connect websocket
        raise HTTPException(status_code=400, detail="Session expired. Please refresh the page.")

    if guess in session.history:
        return {"status": "game_over", "message": f"'{guess}' was already used!"}

    cached = await get_cached_verdict(seed, guess)

    print(f"Using cached verdict: {cached}")

    if cached:
        verdict = cached
    else:
        verdict = await check_if_beats(seed, guess, persona)
        await set_cached_verdict(seed, guess, verdict)

    if verdict == "YES":
        if not session.add_guess(guess):
            return {"status": "game_over", "message": f"'{guess}' already used!"}
        
        async with AsyncSessionLocal() as db:
            try:
                result = await db.execute(select(GlobalGuessCount).where(GlobalGuessCount.guess == guess))
                record = result.scalar_one_or_none()
                if record:
                    record.count += 1
                else:
                    record = GlobalGuessCount(guess=guess, count=1)
                    db.add(record)
                await db.commit()
            except IntegrityError:
                await db.rollback()

        return {
            "status": "success",
            "message": f"✅ Nice! '{guess}' beats '{seed}'. {guess} has been guessed {record.count} times before.",
            "seed_word": guess,
            "score": session.score,
            "history": session.get_history(),
            "global_count": record.count
        }

    return {"status": "fail", "message": f"❌ Nope! '{guess}' doesn’t beat '{seed}'."}

@router.get("/history")
def get_history(session_id: str):
    session = sessions.get(session_id)
    if not session:
        return {"history": []}
    return {"history": session.get_history(), "score": session.score}

@router.post("/reset")
def reset(session_id: str):
    sessions[session_id] = GameSession()
    return {"message": "Game reset."}

# Shared state
active_connections: list[WebSocket] = []
ip_connections: dict[str, int] = defaultdict(int)

@router.websocket("/ws/active_users")
async def websocket_endpoint(websocket: WebSocket):
    ip = websocket.client.host
    # Limit the number of connections per IP address to 5
    if ip_connections[ip] >= 5:
        await websocket.close(code=1008)
        return
    ip_connections[ip] += 1
    # Accept the WebSocket connection
    await websocket.accept()
    active_connections.append(websocket)
    # create a session_id for the user
    session_id = str(id(websocket))
    # Create a new session for the user
    session = GameSession()
    sessions[session_id] = session
    
    try:
        while True:
            if session.is_expired():
                # If the session is expired, remove it and notify the user
                await websocket.send_json({"active_users": len(active_connections), "message": "Session expired. Please refresh the page."})
                break

            # Send the initial message to the user
            await websocket.send_json({"active_users": len(active_connections), "session_id": session_id, "message": "Connected"})
            # keep the connection alive
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print(f"User {session_id} disconnected")
        # Optionally, you can send a message to the disconnected user
        # await websocket.send_json({"active_users": len(active_connections), "message": "Disconnected"})
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Handle disconnection
        if websocket in active_connections:
            active_connections.remove(websocket)
        if session_id in sessions:
            del sessions[session_id]
        # Decrement the connection count for the IP address
        ip_connections[ip] -= 1
        if ip_connections[ip] <= 0:
            del ip_connections[ip]
        # Notify remaining users about the disconnection
        for conn in active_connections:
            if conn != websocket:
                await conn.send_json({"active_users": len(active_connections), "message": f"User {session_id} disconnected"})
        await websocket.close()

@router.get("/active_users")
async def get_active_users():
    return {"active_users": len(active_connections), "sessions": len(sessions), "ip_connections": ip_connections}