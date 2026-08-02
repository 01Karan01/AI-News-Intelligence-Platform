import { motion } from "framer-motion";

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
  const { statistics, errors, hasPartialFailure, loadDashboard } = useEventContext();
  const { todaysEvents, trendingEvents, loading, error } = useEvents();
  const { timeline } = useTimeline();
  const latestEvents = todaysEvents.length > 0 ? todaysEvents : trendingEvents;
  const allFailed = Boolean(errors?.events && errors?.timeline && errors?.statistics);

  if (loading && latestEvents.length === 0 && timeline.length === 0) {
    return (
      <main className={styles.loadingContainer}>
        <div className={styles.spinner} aria-hidden="true" />
        <p>Loading dashboard...</p>
      </main>
    );
  }

  if (allFailed) {
    return (
      <main className={styles.errorContainer}>
        <ErrorState message={error || errors.events} onRetry={loadDashboard} />
      </main>
    );
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

      {hasPartialFailure && <PartialFailureAlert errors={errors} onRetry={loadDashboard} />}

      {errors?.statistics ? (
        <EndpointError title="Statistics" endpoint="/api/statistics" message={errors.statistics} />
      ) : (
        <Statistics statistics={statistics} />
      )}

      {errors?.events ? (
        <EndpointError title="Events" endpoint="/api/events" message={errors.events} />
      ) : loading && latestEvents.length === 0 ? (
        <SkeletonGrid count={4} />
      ) : (
        <TrendingEvents events={latestEvents} />
      )}

      {errors?.timeline ? (
        <EndpointError title="Timeline" endpoint="/api/timeline" message={errors.timeline} />
      ) : loading && timeline.length === 0 ? (
        <SkeletonGrid count={3} />
      ) : (
        <Timeline groups={timeline} />
      )}
    </motion.div>
  );
}

function ErrorState({ message, onRetry }) {
  return (
    <section className={styles.errorState} role="alert">
      <div className={styles.errorIcon} aria-hidden="true">
        !
      </div>
      <h1>Dashboard unavailable</h1>
      <p>{message}</p>
      <div className={styles.errorDetails}>
        <h2>Troubleshooting steps</h2>
        <ul>
          <li>
            Start the backend with <code>python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000</code>.
          </li>
          <li>
            Check <code>http://localhost:8000/api/health</code>.
          </li>
          <li>
            Verify <code>VITE_API_BASE_URL</code> points to <code>http://localhost:8000/api</code>.
          </li>
          <li>Open the browser console for the detailed endpoint error.</li>
        </ul>
      </div>
      <button className={styles.retryButton} type="button" onClick={onRetry}>
        Try Again
      </button>
    </section>
  );
}

function PartialFailureAlert({ errors, onRetry }) {
  const failedEndpoints = Object.entries(errors ?? {})
    .filter(([, message]) => Boolean(message))
    .map(([endpoint]) => endpoint);

  return (
    <section className={styles.partialFailureAlert} role="status">
      <div className={styles.alertIcon} aria-hidden="true">
        !
      </div>
      <div>
        <strong>Some dashboard data failed to load</strong>
        <p>Unable to fetch {failedEndpoints.join(", ")}. Showing the data that is available.</p>
      </div>
      <button className={styles.secondaryButton} type="button" onClick={onRetry}>
        Retry
      </button>
    </section>
  );
}

function EndpointError({ title, endpoint, message }) {
  return (
    <section className={styles.endpointError} role="alert">
      <div>
        <h2>{title}</h2>
        <p>{message}</p>
        <span>Endpoint: {endpoint}</span>
      </div>
    </section>
  );
}

export default Home;
