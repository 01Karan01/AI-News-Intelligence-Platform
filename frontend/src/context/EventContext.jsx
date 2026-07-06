import { useCallback, useMemo, useReducer } from "react";

import { getEvents, getStatistics, getTimeline, searchEvents } from "../services/api";
import { EventContext } from "./EventContextObject";

const initialState = {
  events: [],
  timeline: [],
  statistics: null,
  searchResults: [],
  searchQuery: "",
  loading: false,
  error: "",
};

function eventReducer(state, action) {
  switch (action.type) {
    case "LOAD_START":
      return { ...state, loading: true, error: "" };
    case "LOAD_SUCCESS":
      return {
        ...state,
        loading: false,
        events: action.payload.events,
        timeline: action.payload.timeline,
        statistics: action.payload.statistics,
        searchResults: action.payload.events,
      };
    case "LOAD_ERROR":
      return { ...state, loading: false, error: action.payload };
    case "SEARCH_SUCCESS":
      return { ...state, searchQuery: action.payload.query, searchResults: action.payload.results };
    default:
      return state;
  }
}

export function EventProvider({ children }) {
  const [state, dispatch] = useReducer(eventReducer, initialState);

  const loadDashboard = useCallback(async () => {
    dispatch({ type: "LOAD_START" });
    try {
      const [events, timeline, statistics] = await Promise.all([
        getEvents(),
        getTimeline(),
        getStatistics(),
      ]);
      dispatch({ type: "LOAD_SUCCESS", payload: { events, timeline, statistics } });
    } catch {
      dispatch({
        type: "LOAD_ERROR",
        payload: "News intelligence data could not be loaded. Please try again.",
      });
    }
  }, []);

  const runSearch = useCallback(async (query) => {
    const results = await searchEvents(query);
    dispatch({ type: "SEARCH_SUCCESS", payload: { query, results } });
    return results;
  }, []);

  const value = useMemo(
    () => ({
      ...state,
      loadDashboard,
      runSearch,
    }),
    [loadDashboard, runSearch, state],
  );

  return <EventContext.Provider value={value}>{children}</EventContext.Provider>;
}
