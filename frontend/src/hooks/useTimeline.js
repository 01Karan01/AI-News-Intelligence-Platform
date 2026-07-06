import { useEffect } from "react";

import { useEventContext } from "./useEventContext";

export function useTimeline() {
  const { timeline, loading, error, loadDashboard } = useEventContext();

  useEffect(() => {
    if (timeline.length === 0) {
      loadDashboard();
    }
  }, [loadDashboard, timeline.length]);

  return { timeline, loading, error };
}
