import { useState } from "react";
import { FiArrowRight, FiSearch, FiX } from "react-icons/fi";
import { Link } from "react-router-dom";

import { useSearch } from "../../hooks/useSearch";
import { cleanDisplayText } from "../../utils/text";
import styles from "./SearchBar.module.css";

function SearchBar({ variant = "default" }) {
  const { query, setQuery, results, trendingSearches, isSearching } = useSearch();
  const [focused, setFocused] = useState(false);
  const showPanel = focused || query.length > 0;

  return (
    <div className={`${styles.wrapper} ${styles[variant]}`}>
      <div className={styles.searchBox}>
        <FiSearch className={styles.searchIcon} aria-hidden="true" />
        <input
          type="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => window.setTimeout(() => setFocused(false), 140)}
          placeholder="Search title, summary, people, organizations, locations"
          aria-label="Search news events"
        />
        {query && (
          <button
            className={styles.clearButton}
            type="button"
            aria-label="Clear search"
            onMouseDown={(event) => event.preventDefault()}
            onClick={() => setQuery("")}
          >
            <FiX />
          </button>
        )}
      </div>

      {showPanel && (
        <div className={styles.panel}>
          <div className={styles.panelHeader}>
            <span>{query ? "Matching Events" : "Trending Searches"}</span>
            {isSearching && <small>Searching...</small>}
          </div>

          {!query && (
            <div className={styles.trends}>
              {trendingSearches.map((item) => (
                <button key={item} type="button" onMouseDown={() => setQuery(item)}>
                  {item}
                </button>
              ))}
            </div>
          )}

          {query && (
            <div className={styles.results}>
              {results.length > 0 ? (
                results.slice(0, 5).map((event) => (
                  <Link className={styles.result} key={event.id} to={`/event/${event.id}`}>
                    <span>
                      <strong>{cleanDisplayText(event.title, "Untitled event")}</strong>
                      <small>{event.people.length} people identified</small>
                    </span>
                    <FiArrowRight />
                  </Link>
                ))
              ) : (
                <p className={styles.empty}>No clustered events match this search.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
