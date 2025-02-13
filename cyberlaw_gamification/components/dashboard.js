import React, { useState, useEffect } from "react";
import axios from "axios";
import Chatbot from "./Chatbot";

const API_URL = "http://localhost:5000";

function Dashboard({ token }) {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    const fetchCourses = async () => {
      const response = await axios.get(`${API_URL}/course`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCourses(response.data.courses);
    };
    fetchCourses();
  }, [token]);

  return (
    <div>
      <h2>Dashboard</h2>
      <h3>Courses:</h3>
      <ul>{courses.map((course, index) => <li key={index}>{course}</li>)}</ul>
      <Chatbot token={token} />
    </div>
  );
}

export default Dashboard;
