import { useCallback, useEffect, useMemo, useReducer } from "react";

import { getEvents, getStatistics, getTimeline, searchEvents } from "../services/api";
import { EventContext } from "./EventContextObject";

const initialState = {
  events: [],
  timeline: [],
  statistics: null,
  searchResults: [],
  searchQuery: "",
  loading: true,
  errors: {
    events: null,
    timeline: null,
    statistics: null,
  },
  error: "",
  hasPartialFailure: false,
  lastUpdated: null,
};

const hasError = (errors) => Object.values(errors).some(Boolean);
const allFailed = (errors) => Object.values(errors).every(Boolean);

function eventReducer(state, action) {
  switch (action.type) {
    case "LOAD_START":
      return {
        ...state,
        loading: true,
        error: "",
        errors: { events: null, timeline: null, statistics: null },
        hasPartialFailure: false,
        lastUpdated: null,
      };

    case "LOAD_EVENTS_SUCCESS":
      return {
        ...state,
        events: action.payload,
        searchResults: action.payload,
        errors: { ...state.errors, events: null },
      };

    case "LOAD_EVENTS_ERROR":
      return {
        ...state,
        events: [],
        searchResults: [],
        errors: { ...state.errors, events: action.payload },
      };

    case "LOAD_TIMELINE_SUCCESS":
      return {
        ...state,
        timeline: action.payload,
        errors: { ...state.errors, timeline: null },
      };

    case "LOAD_TIMELINE_ERROR":
      return {
        ...state,
        timeline: [],
        errors: { ...state.errors, timeline: action.payload },
      };

    case "LOAD_STATISTICS_SUCCESS":
      return {
        ...state,
        statistics: action.payload,
        errors: { ...state.errors, statistics: null },
      };

    case "LOAD_STATISTICS_ERROR":
      return {
        ...state,
        statistics: null,
        errors: { ...state.errors, statistics: action.payload },
      };

    case "LOAD_FINISH": {
      const error = allFailed(action.payload.errors)
        ? `All dashboard endpoints failed. ${Object.values(action.payload.errors).join(" | ")}`
        : "";

      return {
        ...state,
        loading: false,
        errors: action.payload.errors,
        error,
        hasPartialFailure: hasError(action.payload.errors),
        lastUpdated: new Date().toISOString(),
      };
    }

    case "SEARCH_SUCCESS":
      return {
        ...state,
        searchQuery: action.payload.query,
        searchResults: action.payload.results,
      };

    case "SEARCH_ERROR":
      return {
        ...state,
        searchQuery: action.payload.query,
        searchResults: [],
      };

    default:
      return state;
  }
}

export function EventProvider({ children }) {
  const [state, dispatch] = useReducer(eventReducer, initialState);

  const loadDashboard = useCallback(async () => {
    console.log("[EventContext] Starting dashboard data load");
    dispatch({ type: "LOAD_START" });

    const results = {
      events: { success: false, error: null },
      timeline: { success: false, error: null },
      statistics: { success: false, error: null },
    };

    try {
      console.log("[EventContext] Fetching /api/events");
      const events = await getEvents();
      console.log(`[EventContext] Loaded ${events.length} events`);
      results.events.success = true;
      dispatch({ type: "LOAD_EVENTS_SUCCESS", payload: events });
    } catch (error) {
      const message = formatAxiosError(error, "events");
      console.error("[EventContext] Events load failed:", message);
      results.events.error = message;
      dispatch({ type: "LOAD_EVENTS_ERROR", payload: message });
    }

    try {
      console.log("[EventContext] Fetching /api/timeline");
      const timeline = await getTimeline();
      console.log(`[EventContext] Loaded ${timeline.length} timeline groups`);
      results.timeline.success = true;
      dispatch({ type: "LOAD_TIMELINE_SUCCESS", payload: timeline });
    } catch (error) {
      const message = formatAxiosError(error, "timeline");
      console.error("[EventContext] Timeline load failed:", message);
      results.timeline.error = message;
      dispatch({ type: "LOAD_TIMELINE_ERROR", payload: message });
    }

    try {
      console.log("[EventContext] Fetching /api/statistics");
      const statistics = await getStatistics();
      console.log("[EventContext] Loaded statistics:", statistics);
      results.statistics.success = true;
      dispatch({ type: "LOAD_STATISTICS_SUCCESS", payload: statistics });
    } catch (error) {
      const message = formatAxiosError(error, "statistics");
      console.error("[EventContext] Statistics load failed:", message);
      results.statistics.error = message;
      dispatch({ type: "LOAD_STATISTICS_ERROR", payload: message });
    }

    const errors = {
      events: results.events.error,
      timeline: results.timeline.error,
      statistics: results.statistics.error,
    };

    dispatch({ type: "LOAD_FINISH", payload: { errors } });
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const runSearch = useCallback(async (query) => {
    try {
      const results = await searchEvents(query);
      dispatch({ type: "SEARCH_SUCCESS", payload: { query, results } });
      return results;
    } catch (error) {
      const message = formatAxiosError(error, "search");
      console.error("[EventContext] Search failed:", message);
      dispatch({ type: "SEARCH_ERROR", payload: { query, error: message } });
      return [];
    }
  }, []);

  const value = useMemo(
    () => ({
      ...state,
      loadData: loadDashboard,
      loadDashboard,
      runSearch,
    }),
    [loadDashboard, runSearch, state],
  );

  return <EventContext.Provider value={value}>{children}</EventContext.Provider>;
}

function formatAxiosError(error, endpoint) {
  if (!error.response) {
    if (error.code === "ERR_NETWORK") {
      return `Network error while loading ${endpoint}. Backend unreachable at http://localhost:8000.`;
    }

    if (error.code === "ECONNABORTED") {
      return `Request timeout while loading ${endpoint} after ${error.config?.timeout}ms.`;
    }

    return `Connection failed while loading ${endpoint}: ${error.message}`;
  }

  const status = error.response.status;
  const data = error.response.data;
  const detail = data?.detail || data?.message || error.message;

  if (status === 404) {
    return `Endpoint not found for ${endpoint} (404): ${error.config?.url}`;
  }

  if (status === 500) {
    return `Server error while loading ${endpoint} (500): ${detail}`;
  }

  if (status === 503) {
    return `Service unavailable while loading ${endpoint} (503). Backend may be down or restarting.`;
  }

  if (status >= 400 && status < 500) {
    return `Client error while loading ${endpoint} (${status}): ${detail}`;
  }

  if (status >= 500) {
    return `Server error while loading ${endpoint} (${status}): ${detail}`;
  }

  return `Failed to load ${endpoint}: ${error.message}`;
}
