import React, { useState } from "react";
import bgImg from "../assets/img/gameintro.jpg";
import charImg from "../assets/img/gameintro.jpg";
import asteroidImg from "../assets/img/asteroid.png";

const questions = [
  {
    text: "I am an asteroid heading to a big population density! What should I do?",
    options: ["Divert path", "Explode myself", "Do nothing"],
    correct: 0,
  },
  {
    text: "I am an asteroid with high velocity. What's the best action?",
    options: ["Slow down", "Change orbit", "Crash directly"],
    correct: 1,
  },
  {
    text: "I might hit the ocean. What is the main risk?",
    options: ["Tsunami", "Nothing happens", "Forest fire"],
    correct: 0,
  },
];

const Game = () => {
  const [currentQ, setCurrentQ] = useState(0);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState("");

  const handleAnswer = (i) => {
    if (i === questions[currentQ].correct) {
      setScore(score + 1);
      setFeedback("✅ Correct!");
    } else {
      setFeedback("❌ Wrong!");
    }

    setTimeout(() => {
      setFeedback("");
      setCurrentQ((prev) => (prev + 1) % questions.length);
    }, 1500);
  };

  return (
    <div className="game-container" style={{ backgroundImage: `url(${bgImg})` }}>
      <style>{`
        .game-container {
          width: 100%;
          height: 100vh;
          color: white;
          position: relative;
          overflow: hidden;
          background-size: cover;
          display: flex;
          flex-direction: column;
        }

        .score-feedback {
          position: absolute;
          top: 20px;
          left: 50%;
          transform: translateX(-50%);
          text-align: center;
          font-size: 28px;
          font-weight: bold;
          z-index: 10;
        }

        .game-content {
          display: flex;
          flex-direction: column;
          flex-grow: 1;
          justify-content: flex-start;
          padding: 40px;
        }

        .asteroid-section {
          display: flex;
          align-items: flex-start;
          gap: 30px;
          margin-bottom: auto;
        }

        .asteroid {
          width: 200px;
          animation: bounce 2s infinite;
          filter: drop-shadow(0px 4px 15px black);
        }

        .question-box {
          background: rgba(0, 0, 0, 0.75);
          border: 2px solid #d84594;
          padding: 35px;
          border-radius: 18px;
          font-size: 28px;
          font-weight: 600;
          max-width: 650px;
          line-height: 1.5;
          box-shadow: 0 0 20px rgba(216, 69, 148, 0.6);
          text-align: left;
        }

        .choices-section {
          display: flex;
          flex-direction: column;
          gap: 25px;
          width: 320px;
          margin-top: auto;
          margin-bottom: 50px;
          align-self: flex-end; /* moves choices to right */
        }

        .choice-btn {
          padding: 20px;
          font-size: 22px;
          font-weight: bold;
          border-radius: 16px;
          border: none;
          cursor: pointer;
          background: linear-gradient(to right, #d84594, #6b21a8);
          color: white;
          transition: transform 0.2s, box-shadow 0.2s;
        }

        .choice-btn:hover {
          transform: scale(1.05);
          box-shadow: 0 0 20px rgba(216, 69, 148, 0.7);
        }

        .character {
          position: absolute;
          bottom: 20px;
          left: 20px;
          text-align: center;
        }

        .character-img {
          width: 180px;
          filter: drop-shadow(0px 4px 12px black);
        }

        .character-text {
          background: rgba(0, 0, 0, 0.7);
          margin-top: 10px;
          padding: 10px 14px;
          border-radius: 12px;
          font-size: 20px;
        }

        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-15px); }
        }
      `}</style>

      <div className="score-feedback">
        <p>Score: {score}</p>
        <p>{feedback}</p>
      </div>

      <div className="game-content">
        {/* Asteroid + Question top-left */}
        <div className="asteroid-section">
          <img src={asteroidImg} alt="asteroid" className="asteroid" />
          <div className="question-box">{questions[currentQ].text}</div>
        </div>

        {/* Choices pinned at bottom-right */}
        <div className="choices-section">
          {questions[currentQ].options.map((opt, i) => (
            <button key={i} onClick={() => handleAnswer(i)} className="choice-btn">
              {opt}
            </button>
          ))}
        </div>
      </div>

      <div className="character">
        <img src={charImg} alt="character" className="character-img" />
        <p className="character-text">I'm ready to help!</p>
      </div>
    </div>
  );
};

export default Game;
