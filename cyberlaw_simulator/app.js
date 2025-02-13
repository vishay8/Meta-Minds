import React, { useState, useEffect } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const App = () => {
    const [scenario, setScenario] = useState("");
    const [userAnswer, setUserAnswer] = useState("");
    const [score, setScore] = useState(0);
    const [username, setUsername] = useState("");
    const [leaderboard, setLeaderboard] = useState([]);

    useEffect(() => {
        fetchScenario();
        fetchLeaderboard();
    }, []);

    const fetchScenario = async () => {
        const response = await axios.get("http://127.0.0.1:5000/get_scenario");
        setScenario(response.data.scenario);
    };

    const submitResponse = async () => {
        const response = await axios.post("http://127.0.0.1:5000/submit_response", {
            username,
            user_answer: userAnswer,
            correct_answer: "Correct Legal Action"
        });

        toast(response.data.message);
        setScore(response.data.score);
        fetchLeaderboard();
    };

    const fetchLeaderboard = async () => {
        const response = await axios.get("http://127.0.0.1:5000/leaderboard");
        setLeaderboard(response.data);
    };

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>AI Cyber Law Training Simulator</h1>
            <input 
                type="text" 
                placeholder="Enter Username" 
                onChange={(e) => setUsername(e.target.value)}
            />
            <h3>Scenario:</h3>
            <p>{scenario}</p>
            <input 
                type="text" 
                placeholder="Your Answer" 
                onChange={(e) => setUserAnswer(e.target.value)}
            />
            <button onClick={submitResponse}>Submit</button>
            <h3>Your Score: {score}</h3>

            <h3>Leaderboard</h3>
            <ul>
                {leaderboard.map((user, index) => (
                    <li key={index}>{user.username} - {user.score} points</li>
                ))}
            </ul>
            <ToastContainer />
        </div>
    );
};

export default App;
