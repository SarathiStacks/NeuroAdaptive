import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Learn from "./pages/Learn";
import Progress from "./pages/Progress";
import Reader from "./pages/Reader";
import Achievements from "./pages/Achievements"; // ✔ ADD THIS
import Handwriting from "./pages/Handwriting";
import Quiz from "./pages/Quiz";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Main Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/learn" element={<Learn />} />
        <Route path="/progress" element={<Progress />} />
        <Route path="/handwriting" element={<Handwriting />} />

        {/* Learning Module Routes */}
        <Route path="/reader" element={<Reader />} />
        <Route path="/quiz" element={<Quiz />} /> 
        <Route path="/achievements" element={<Achievements />} /> {/* ✔ ADD THIS */}
      </Routes>
    </BrowserRouter>
  );
}
