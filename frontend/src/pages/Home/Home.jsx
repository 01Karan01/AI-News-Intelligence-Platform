import { motion } from "framer-motion";

import ErrorState from "../../components/Error/ErrorState";
import Hero from "../../components/Hero/Hero";
import SkeletonGrid from "../../components/Loading/SkeletonGrid";
import Statistics from "../../components/Statistics/Statistics";
import Timeline from "../../components/Timeline/Timeline";
import TrendingEvents from "../../components/TrendingEvents/TrendingEvents";
import { useEventContext } from "../../hooks/useEventContext";
import { useEvents } from "../../hooks/useEvents";
import { useTimeline } from "../../hooks/useTimeline";
import styles from "./Home.module.css";

function Home() {
  const { statistics } = useEventContext();
  const { todaysEvents, trendingEvents, loading, error } = useEvents();
  const { timeline } = useTimeline();
  const eventsForToday = todaysEvents.length > 0 ? todaysEvents : trendingEvents;

  if (error) {
    return <ErrorState title="Dashboard unavailable" message={error} />;
  }

  return (
    <motion.div
      className={styles.page}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.24 }}
    >
      <Hero />
      <Statistics statistics={statistics} />
      {loading && eventsForToday.length === 0 ? (
        <SkeletonGrid count={4} />
      ) : (
        <TrendingEvents events={eventsForToday} />
      )}
      {loading && timeline.length === 0 ? <SkeletonGrid count={3} /> : <Timeline groups={timeline} />}
    </motion.div>
  );
}

export default Home;
