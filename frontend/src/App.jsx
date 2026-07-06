import { lazy, Suspense } from "react";
import { AnimatePresence } from "framer-motion";
import { Route, Routes, useLocation } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import PageLoader from "./components/Loading/PageLoader";

const Home = lazy(() => import("./pages/Home/Home"));
const Event = lazy(() => import("./pages/Event/Event"));
const About = lazy(() => import("./pages/About/About"));
const NotFound = lazy(() => import("./pages/NotFound/NotFound"));

function App() {
  const location = useLocation();

  return (
    <Suspense fallback={<PageLoader label="Preparing NewsLens AI" />}>
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route element={<MainLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="/event/:id" element={<Event />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </AnimatePresence>
    </Suspense>
  );
}

export default App;
