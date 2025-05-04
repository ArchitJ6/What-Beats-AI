import JSConfetti from "js-confetti";
import { useEffect, useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import Loader from "./components/Loader";

const API_URL = import.meta.env.VITE_API_URL;
const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL;

function App() {
  const jsConfetti = new JSConfetti();
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState<string[]>([]);
  const [score, setScore] = useState(0);
  const [seedWord, setSeedWord] = useState("rock");
  const [guess, setGuess] = useState("");
  const [showLoading, setShowLoading] = useState(true);
  const [activeUsers, setActiveUsers] = useState(0);
  const [isConnected, setIsConnected] = useState(false);
  const [sessionId, setSessionId] = useState<string>("");
  const [persona, setPersona] = useState<string>("serious");
  const [message, setMessage] = useState<string>("");
  const [formDisabled, setFormDisabled] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(`${WS_BASE_URL}/active_users`);

    ws.onopen = () => {
      console.log("WebSocket connection established");
      setIsConnected(true);
    };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setActiveUsers(data.active_users);
      setSessionId(data.session_id);
      setShowLoading(false);
    };
    ws.onclose = () => {
      console.log("WebSocket connection closed");
      setIsConnected(false);
      setShowLoading(false);
      setFormDisabled(true);
    };
    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setIsConnected(false);
      setShowLoading(false);
      toast.error("Failed to connect to the server. Please refresh the page.");
      setFormDisabled(true);
    };

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const submitGuess = async () => {
    if (!sessionId) {
      toast.error("Something went wrong! Please refresh the page.");
      return;
    }
    if (guess.trim() === "") return;
    setShowLoading(true);
    try {
      const response = await fetch(`${API_URL}/guess`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          guess: guess,
          seed: seedWord,
          session_id: sessionId,
          persona: persona,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        if (data.status === "success") {
          console.log("Guess submitted successfully:", data);
          setScore(data.score);
          setHistory(data.history);
          setSeedWord(data.seed_word);
          setGuess("");
          setMessage(data.message);
          jsConfetti.addConfetti({
            emojis: ["🌈", "⚡️", "💥", "✨", "💫"],
            emojiSize: 50,
            confettiNumber: 70,
          });
        } else if (data.status === "game_over") {
          setMessage(
            "Game Over! " + data.message + " Reset the game to play again."
          );
          setFormDisabled(true);
          jsConfetti.addConfetti({
            emojis: ["💔", "😢"],
            emojiSize: 50,
            confettiNumber: 70,
          });
        } else {
          setMessage(data.message || "Something went wrong!");
          setFormDisabled(true);
          jsConfetti.addConfetti({
            emojis: ["💔", "😢"],
            emojiSize: 50,
            confettiNumber: 70,
          });
        }
      } else {
        const errorData = await response.json();
        setMessage(errorData.message || "Something went wrong!");
        setFormDisabled(true);
        jsConfetti.addConfetti({
          emojis: ["💔", "😢"],
          emojiSize: 50,
          confettiNumber: 70,
        });
      }
    } catch (error) {
      console.error("Error submitting guess:", error);
      setFormDisabled(true);
      setMessage("Failed to connect to the server. Please refresh the page.");
      jsConfetti.addConfetti({
        emojis: ["💔", "😢"],
        emojiSize: 50,
        confettiNumber: 70,
      });
    }
    setShowLoading(false);
  };

  const resetGame = async () => {
    if (!sessionId) {
      toast.error("Something went wrong! Please refresh the page.");
      return;
    }
    setShowLoading(true);
    try {
      const response = await fetch(`${API_URL}/reset?session_id=${sessionId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data = await response.json();
        if (data.message !== "Game reset.") {
          toast.error("Something went wrong! Please refresh the page.");
          return;
        } else {
          toast.success("Game reset successfully!");
          setScore(0);
          setHistory([]);
          setSeedWord("rock");
          setGuess("");
          setMessage("");
          setFormDisabled(false);
          setShowHistory(false);
        }
      } else {
        const errorData = await response.json();
        toast.error(errorData.message || "Something went wrong!");
      }
    } catch (error) {
      console.error("Error resetting game:", error);
      toast.error("Failed to connect to the server. Please refresh the page.");
    }
    setShowLoading(false);
  };

  return (
    <>
      <main className="max-w-2xl relative gap-3 m-auto p-8 rounded-2xl shadow-2xl w-full flex flex-col items-center justify-center">
        <p className="absolute top-5 left-5 text-sm text-gray-500">
          {isConnected ? `Active Users: ${activeUsers}` : "Connecting..."}
        </p>

        <div className="absolute top-5 right-5 text-sm text-gray-500">
          <select
            className="p-1 outline-none rounded-md text-lg border-2 border-solid border-[#ccc]"
            value={persona}
            onChange={(e) => {
              setPersona(e.target.value);
              resetGame();
            }}
          >
            <option value="serious">Serious</option>
            <option value="funny">Cheery</option>
          </select>
        </div>

        <h1 className="text-4xl font-bold mt-4">🪨 What Beats AI?</h1>
        <p id="prompt" className="text-lg">
          Your seed is: <strong>{seedWord}</strong>
        </p>

        <div className="w-full flex flex-row gap-1 justify-center items-center">
          <input
            type="text"
            className="p-1 outline-none rounded-md text-lg w-3/5 border-2 border-solid border-[#ccc] disabled:bg-[#f3f4f6] disabled:text-gray-500"
            id="guess-input"
            placeholder="Enter your guess..."
            required
            disabled={formDisabled}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                submitGuess();
              }
            }}
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
          />
          <button
            disabled={formDisabled}
            className="px-4 py-2 bg-[#4ade80] text-white rounded-md cursor-pointer hover:bg-[#22c55e] transition-all duration-500 disabled:bg-[#a1a1aa] disabled:cursor-not-allowed"
            onClick={submitGuess}
          >
            Submit
          </button>
        </div>

        <div className="w-full flex flex-col items-center justify-center my-2 mb-0">
          <h2>Score: {score}</h2>
        </div>

        {message && (
          <div
            className={`w-full flex flex-col items-center justify-center my-2 mt-0 p-2 rounded-md`}
          >
            <h3 className="text-lg">{message}</h3>
          </div>
        )}

        <div className="flex flex-row gap-2">
          <button
            onClick={() => {
              setShowHistory(!showHistory);
            }}
            className="px-4 py-2 bg-[#4ade80] text-white rounded-md cursor-pointer hover:bg-[#22c55e] transition-all duration-500"
          >
            {showHistory ? "Hide History" : "Show History"}
          </button>
          <button
            onClick={resetGame}
            className="px-4 py-2 bg-[#f87171] text-white rounded-md cursor-pointer hover:bg-[#ef4444] transition-all duration-500"
          >
            Reset
          </button>
        </div>

        {showHistory && (
          <section
            id="history-section"
            className="w-full flex flex-col items-center justify-center my-2"
          >
            <h3 className="text-lg">Already Guessed:</h3>
            <p className="text-base">
              {history.length > 0 ? (
                history
                  .slice()
                  .reverse()
                  .map((item, index) => (
                    <span key={index}>
                      {item}
                      {index < history.length - 1 ? " 🤜 " : ""}
                    </span>
                  ))
              ) : (
                <span>No guesses yet!</span>
              )}
            </p>
          </section>
        )}
      </main>

      {showLoading && <Loader />}
      <ToastContainer />
    </>
  );
}

export default App;
