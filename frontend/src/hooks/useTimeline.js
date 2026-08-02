import { useEventContext } from "./useEventContext";

export function useTimeline() {
  const { timeline, loading, error, loadDashboard } = useEventContext();

  return { timeline, loading, error, refresh: loadDashboard };
}

