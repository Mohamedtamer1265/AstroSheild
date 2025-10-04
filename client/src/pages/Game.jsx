import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import gameBg from "../assets/img/without.png";
import attackImg from "../assets/img/attack.png";
import neoImg from "../assets/img/neo.png";
import questionsData from "../questions.json";

// ✅ Sounds
import youDidItSound from "../assets/sound/good.mp3";
import failSound from "../assets/sound/fail.mp3";

function Game() {
  const [availableQuestions, setAvailableQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [completedCount, setCompletedCount] = useState(0);
  const [attackAnimating, setAttackAnimating] = useState(false);

  const navigate = useNavigate();

  // ✅ Universal sound player
  const playSound = (src) => {
    const audio = new Audio(src);
    audio.volume = 0.8;
    audio.play().catch((err) => console.log("Audio error:", err));
  };

  // ✅ Shuffle questions initially
  useEffect(() => {
    const shuffled = [...questionsData].sort(() => Math.random() - 0.5);
    setAvailableQuestions(shuffled);
    setCurrentQuestion(shuffled[0]);
  }, []);

  // ✅ Pick new random question
  const getRandomQuestion = () => {
    if (availableQuestions.length === 0) {
      const reshuffled = [...questionsData].sort(() => Math.random() - 0.5);
      setAvailableQuestions(reshuffled);
      setCurrentQuestion(reshuffled[0]);
      setCompletedCount(0);
      return;
    }
    const randomIndex = Math.floor(Math.random() * availableQuestions.length);
    setCurrentQuestion(availableQuestions[randomIndex]);
  };

  // ✅ Answer logic
  const handleAnswerClick = (answer) => {
    setSelectedAnswer(answer);
    setShowResult(true);
    const correct = answer === currentQuestion.correct_answer;
    setIsCorrect(correct);

    if (correct) {
      playSound(youDidItSound);
      setAttackAnimating(true);

      const newAvailable = availableQuestions.filter(
        (q) => q.id !== currentQuestion.id
      );
      setAvailableQuestions(newAvailable);
      setCompletedCount((c) => c + 1);
    } else {
      playSound(failSound);
    }
  };

  // ✅ Move to next question
  const handleNext = () => {
    setSelectedAnswer(null);
    setShowResult(false);
    setIsCorrect(false);
    if (isCorrect) {
      getRandomQuestion();
    }
  };

  if (!currentQuestion) {
    return (
      <div className="h-screen w-full flex items-center justify-center text-white">
        Loading...
      </div>
    );
  }

  const choiceLabels = ["A", "B", "C", "D"];
  const choices = currentQuestion.choices
    .map((choiceObj, index) => {
      const choiceKey = `choice_${choiceLabels[index].toLowerCase()}`;
      return {
        label: choiceLabels[index],
        text: choiceObj[choiceKey] || "",
      };
    })
    .filter((choice) => choice.text);

  return (
    <div
      className="h-screen w-full bg-cover bg-center relative text-white overflow-hidden"
      style={{ backgroundImage: `url(${gameBg})` }}
    >
      {/* ✅ Galaxy Back Button */}
      <button
        onClick={() => navigate("/")}
        className="absolute top-6 left-6 z-50 px-5 py-2 
        bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-600 
        rounded-full font-bold text-white shadow-[0_0_20px_rgba(0,200,255,0.7)] 
        hover:from-cyan-500 hover:via-blue-600 hover:to-indigo-700 transition-all duration-300"
      >
        ⬅ Back
      </button>

      {/* ✅ Attack Animation */}
      <style>
        {`
          @keyframes attackMoveDown {
            0% {
              top: 5%;
              transform: scale(1);
              opacity: 1;
            }
            50% {
              transform: scale(1.3);
            }
            100% {
              top: 120%;
              transform: scale(1.5);
              opacity: 0;
            }
          }
          .attack-animate {
            animation: attackMoveDown 3s ease-in-out forwards;
          }
        `}
      </style>

      {/* 🌠 Falling Asteroid */}
      <img
        src={attackImg}
        alt="Asteroid"
        className={`absolute z-50 ${
          attackAnimating ? "attack-animate" : ""
        }`}
        style={{
          width: "230px",
          height: "230px",
          top: "8%",
          right: "8%",
        }}
        onAnimationEnd={() => setAttackAnimating(false)}
      />

      {/* 🧑‍🚀 NEO Character beside the question box */}
      <img
        src={neoImg}
        alt="Neo"
        className="absolute bottom-10 left-10 z-20"
        style={{
          width: "300px",
          transform: "scaleX(-1)", // ✅ Flips character to face left
          filter: "drop-shadow(0 0 10px rgba(0,200,255,0.7))",
        }}
      />

      {/* ❌ Try Again Modal */}
      {showResult && !isCorrect && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/70 backdrop-blur-sm">
          <div
            className="absolute inset-0 pointer-events-none 
            bg-[radial-gradient(circle_at_30%_30%,rgba(0,180,255,0.15),transparent_70%),radial-gradient(circle_at_70%_70%,rgba(180,0,255,0.15),transparent_80%)] animate-pulse"
          />
          <div
            className="relative bg-gradient-to-b from-blue-900/90 via-indigo-900/80 to-black/90
            border border-cyan-400/40 rounded-2xl p-8 max-w-md mx-4 text-center
            shadow-[0_0_40px_rgba(0,200,255,0.6)]"
          >
            <div
              className="absolute -top-10 left-1/2 -translate-x-1/2 w-20 h-20 flex items-center justify-center 
              rounded-full bg-gradient-to-br from-red-600 to-pink-500 
              border-4 border-red-300 shadow-[0_0_30px_rgba(255,100,100,0.9)]"
            >
              <span className="text-4xl font-extrabold text-white">❌</span>
            </div>
            <h2 className="text-3xl font-bold mb-4 mt-12 text-cyan-300 drop-shadow-[0_0_10px_rgba(0,200,255,0.8)]">
              Try Again!
            </h2>
            <p className="text-lg mb-6 text-blue-100 leading-relaxed drop-shadow-[0_0_6px_rgba(150,200,255,0.6)]">
              That’s not the correct answer. Don’t give up — the galaxy still believes in you!
            </p>
            <button
              onClick={handleNext}
              className="bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-600 text-white px-10 py-3 
              rounded-full font-bold shadow-[0_0_25px_rgba(0,200,255,0.6)] 
              hover:from-cyan-500 hover:via-blue-600 hover:to-indigo-700 transition-all duration-500"
            >
              🌌 Try Again
            </button>
          </div>
        </div>
      )}

      {/* 🌌 Question Box */}
      <div className="absolute bottom-0 left-0 right-0 z-10 p-6">
        <div className="max-w-6xl mx-auto p-6 rounded-2xl border border-cyan-400 bg-[rgba(40,77,128,0.3)] backdrop-blur-md shadow-2xl">
          <h2 className="text-xl font-bold text-center mb-2 text-cyan-300">
            {currentQuestion.scenario_title}
          </h2>
          <div className="text-center text-sm mb-4 text-cyan-200">
            <p>
              <strong>Asteroid:</strong> {currentQuestion.asteroid_info.name} |{" "}
              <strong>Size:</strong> {currentQuestion.asteroid_info.size} |{" "}
              <strong>Warning Time:</strong>{" "}
              {currentQuestion.asteroid_info.warning_time}
            </p>
          </div>
          <p className="text-center text-lg mb-6">{currentQuestion.question}</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            {choices.map((choice, index) => (
              <button
                key={`${choice.label}-${index}`}
                onClick={() => handleAnswerClick(choice.text)}
                disabled={showResult}
                className={`flex items-center px-4 py-3 rounded-full border text-left transition ${
                  showResult && isCorrect
                    ? choice.text === currentQuestion.correct_answer
                      ? "border-green-400 bg-green-500/30"
                      : "border-cyan-400 opacity-50"
                    : "border-cyan-400 hover:bg-[rgba(21,238,255,0.1)] cursor-pointer"
                }`}
              >
                <span className="mr-3 font-bold">{choice.label}</span>
                {choice.text}
              </button>
            ))}
          </div>

          {showResult && isCorrect && (
            <div className="mt-4 p-4 rounded-lg bg-[rgba(0,0,0,0.3)]">
              <p className="text-center font-bold text-xl mb-2">
                <span className="text-green-400">✓ Correct!</span>
              </p>
              <p className="text-sm text-cyan-100 mb-3">
                <strong>Explanation:</strong> {currentQuestion.justification}
              </p>
              <button
                onClick={handleNext}
                className="w-full py-2 rounded-full font-bold transition bg-green-500 hover:bg-green-600"
              >
                Next Question
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Game;
