# 🎮 **What Beats AI – GenAI Game** 🤖

## 🚀 **Introduction**

**What Beats AI** is an interactive word-challenge game that leverages **Generative AI** (GenAI) to judge whether a player's guess can beat a given seed word. 🎯 The game allows players to make guesses and get real-time feedback through a dynamic, AI-driven experience. 🧠💥 Players score points by making valid and winning guesses, and can compete with others in a fun, fast-paced environment! 🌐

## 📝 **Features** ✨

* **AI-Powered Judgement** 🤖: Uses a language model to assess if a guess beats a seed word.
* **Real-Time Multiplayer** ⏱️: Players can join, interact, and compete in real time through WebSockets.
* **Profanity Filtering** 🚫: Automatically checks and filters inappropriate content.
* **Game History & Scores** 🏆: Tracks guess history and scores for every session.
* **Global Guess Count** 🌍: Monitors how many times each guess has been made globally.
* **Session Management** ⏳: Handles unique sessions, timeouts, and expirations.
* **Database-Driven** 📊: Uses PostgreSQL for storing guess statistics and game data.
* **Cache Integration** ⚡: Redis ensures quick response times by caching game verdicts.
* **Dockerized** 🐳: The whole app is containerized for easy deployment and scalability.

## 🔧 **Tech Stack** ⚙️

* **Backend**: FastAPI 🚀
* **Frontend**: React + Vite ⚛️
* **Database**: PostgreSQL 🗄️ (with SQLAlchemy ORM)
* **Cache**: Redis 🧑‍💻
* **Profanity Filter**: `profanity_check` 🧹
* **WebSockets**: Real-time communication 🌐
* **Docker**: Containerization 🐳
* **Docker Compose**: Multi-service orchestration 🔄

## 📂 **Project Structure**

```
What Beats AI – GenAI Game/
├── backend/  
│   ├── api/ 
│   │   └── routes.py           # API endpoints for handling game logic
│   ├── core/                  
│   │   ├── ai_client.py        # Communicates with the LLM (AI client)
│   │   ├── cache.py            # Redis helpers for caching verdicts
│   │   ├── game_logic.py       # Game logic, session management, and validation
│   │   └── moderation.py       # Profanity check and policy enforcement
│   ├── db/
│   │   ├── models.py           # Database models for global guess count
│   │   └── session.py          # SQLAlchemy session management
│   └── main.py                 # FastAPI app entry point
├── frontend/
│   └── React Vite code         # Frontend code (React with Vite)
├── tests/
│   └── e2e_duplicate_test.py   # End-to-end testing
├── Dockerfile                  # Docker configuration for backend
├── docker-compose.yml          # Multi-service Docker Compose file
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🏃‍♂️ **Getting Started** 🏁

### 1. **Clone the Repository** 💻

Clone the repository to your local machine:

```bash
git clone https://github.com/ArchitJ6/What-Beats-AI.git
cd What-Beats-AI
```

### 2. **Create Environment Files** 📄

Create `.env` files in the root and frontend directories. These files should be based on the `.env.example` provided:

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```

Make sure to update the environment variables with the correct configuration, such as database URLs, Redis configuration, and other necessary settings.

### 3. **Build and Run the Application Using Docker** 🐋

To build and run the application with Docker, execute the following command:

```bash
docker-compose up --build
```

This command will:

* Build all necessary Docker images 🚀
* Set up the backend, frontend, Redis, and PostgreSQL services 🔧
* Run the application on your local machine 🖥️

### 4. **Access the Application** 🌍

Once the services are up, you can access the game by visiting the following URL in your browser:

```
http://localhost:5173 (Frontend)
http://localhost:8000 (Backend)
```

The frontend will automatically interact with the backend via API calls and WebSockets, allowing you to play the game! 🎮

## ⚡ **API Endpoints** 🔌

### 1. **POST `/guess`** 🎯

This endpoint allows the user to submit a guess to beat the seed word. It returns the result of the game (whether the guess is valid and if it beats the seed).

**Request Body**:

```json
{
    "seed": "apple",
    "guess": "banana",
    "session_id": "unique-session-id",
    "persona": "serious"
}
```

**Response**:

```json
{
    "status": "success",
    "message": "✅ Nice! 'banana' beats 'apple'. 'banana' has been guessed 15 times before.",
    "seed_word": "banana",
    "score": 10,
    "history": ["rock", "banana"],
    "global_count": 15
}
```

### 2. **GET `/history`** 📜

This endpoint retrieves the guess history and score of a session.

**Request**:

```bash
GET /history?session_id=unique-session-id
```

**Response**:

```json
{
    "history": ["rock", "banana"],
    "score": 10
}
```

### 3. **POST `/reset`** 🔄

Resets the game for the current session.

**Request**:

```bash
POST /reset?session_id=unique-session-id
```

**Response**:

```json
{
    "message": "Game reset."
}
```

### 4. **WebSocket `/ws/active_users`** 🌐

This WebSocket endpoint provides real-time updates on the number of active users.

### 5. **GET `/active_users`** 👥

This endpoint retrieves the current count of active users and sessions.

**Response**:

```json
{
    "active_users": 10,
    "sessions": 12,
    "ip_connections": {
        "192.168.1.1": 3,
        "192.168.1.2": 2
    }
}
```

## 💡 **Game Logic** 🧠

The game operates by accepting user guesses and comparing them against a pre-generated seed word. The judgment is made using an AI language model, and the results are cached for faster responses. Sessions are managed with a timeout feature, ensuring that players are disconnected after periods of inactivity ⏳.

## 🧑‍💻 **Developing and Testing** 🛠️

To test the application locally, follow these steps:

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   After setting up Docker and environment files, start the app using:

   ```bash
   docker-compose up
   ```

3. **Test API Endpoints** 🧪:
   Use tools like Postman or Insomnia to test the API endpoints.

4. **Run End-to-End Tests** 🏅:
   End-to-end tests are located in the `tests/e2e_duplicate_test.py` file. Run them using:

   ```bash
   pytest
   ```

## 📦 **Docker & Services** 🐋

* **Backend**: FastAPI 🚀 for API management and game logic.
* **Frontend**: React ⚛️ with Vite for a fast, responsive UI.
* **Database**: PostgreSQL 🗄️ to store global guess counts and session data.
* **Redis**: Fast, in-memory caching for quick access to previous verdicts ⚡.
* **WebSockets**: Real-time communication for active player updates 🌐.

## 💬 **Contributing** 🌟

We welcome contributions! 💥 To contribute to this project, please follow these steps:

1. Fork the repository 🍴.
2. Create a new branch (`git checkout -b feature-name`) 🌱.
3. Make your changes 🖋️.
4. Commit your changes (`git commit -am 'Add feature'`) 💬.
5. Push to the branch (`git push origin feature-name`) 🚀.
6. Create a pull request 🔀.

## 🛠 **Technologies Used** 💻

* **Backend**: FastAPI 🚀, SQLAlchemy 🗄️, Redis 🧑‍💻
* **Frontend**: React ⚛️, Vite ⚡
* **Database**: PostgreSQL 🗄️
* **Cache**: Redis 🧑‍💻
* **Real-Time Communication**: WebSockets 🌐
* **Profanity Filtering**: `profanity_check` 🧹

## 📜 **License** ⚖️

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.