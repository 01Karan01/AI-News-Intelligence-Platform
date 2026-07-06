import { useEffect, useMemo } from "react";

import { useEventContext } from "./useEventContext";

export function useEvents() {
  const { events, loading, error, loadDashboard } = useEventContext();

  useEffect(() => {
    if (events.length === 0) {
      loadDashboard();
    }
  }, [events.length, loadDashboard]);

  const todaysEvents = useMemo(() => {
    const today = new Date().toDateString();
    return events.filter((event) => new Date(event.date).toDateString() === today);
  }, [events]);

  const trendingEvents = useMemo(
    () => [...events].sort((a, b) => b.articleCount - a.articleCount).slice(0, 4),
    [events],
  );

  return { events, todaysEvents, trendingEvents, loading, error, refresh: loadDashboard };
}
