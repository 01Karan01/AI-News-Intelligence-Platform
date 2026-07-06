import { useCallback, useMemo, useState } from "react";

import { useEventContext } from "./useEventContext";

export const TRENDING_SEARCHES = ["AI", "Iran", "Trump", "GTA 6", "OpenAI"];

export function useSearch() {
  const { searchResults, runSearch } = useEventContext();
  const [query, setLocalQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  const setQuery = useCallback(
    async (value) => {
      setLocalQuery(value);
      setIsSearching(true);
      try {
        return await runSearch(value);
      } finally {
        setIsSearching(false);
      }
    },
    [runSearch],
  );

  const trendingSearches = useMemo(() => {
    const term = query.toLowerCase();
    const matches = TRENDING_SEARCHES.filter((item) => item.toLowerCase().includes(term));
    return matches.length > 0 ? matches : TRENDING_SEARCHES;
  }, [query]);

  return { query, setQuery, results: searchResults, isSearching, trendingSearches };
}
