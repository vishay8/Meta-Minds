import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:5000";

function Chatbot({ token }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;
    setMessages([...messages, { text: input, user: true }]);
    setInput("");

    const response = await axios.post(`${API_URL}/chatbot`, { message: input }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    setMessages([...messages, { text: input, user: true }, { text: response.data.reply, user: false }]);
  };

  return (
    <div>
      <h2>AI Chatbot</h2>
      <div>{messages.map((msg, index) => <p key={index}>{msg.text}</p>)}</div>
      <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask something..." />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chatbot;
