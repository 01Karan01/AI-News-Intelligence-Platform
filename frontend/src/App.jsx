import { Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Home from "./pages/Home/Home";
import Event from "./pages/Event/Event";
import About from "./pages/About/About";

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Home />} />

        <Route path="/event/:id" element={<Event />} />

        <Route path="/about" element={<About />} />
      </Route>
    </Routes>
  );
}

export default App;