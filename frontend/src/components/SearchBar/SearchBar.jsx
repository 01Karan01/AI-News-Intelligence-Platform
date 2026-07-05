import { useState } from "react";
import { useNavigate } from "react-router-dom";

import events from "../../data/events";

import styles from "./SearchBar.module.css";

function SearchBar() {

    const [query, setQuery] = useState("");

    const navigate = useNavigate();

    const filteredEvents = events.filter(event =>
        event.title.toLowerCase().includes(query.toLowerCase())
    );

    return (

        <div className={styles.searchContainer}>

            <input
                type="text"
                placeholder="🔍 Search AI Events..."
                value={query}
                onChange={(e)=>setQuery(e.target.value)}
            />

            <div className={styles.dropdown}>

                {query === "" ? (

                    <>
                        <h4>🔥 Trending Searches</h4>

                        <div className={styles.tags}>

                            <button>🤖 AI</button>
                            <button>🌍 Iran</button>
                            <button>🎮 GTA 6</button>
                            <button>🏛️ Trump</button>

                        </div>

                    </>

                ) : (

                    filteredEvents.map(event=>(
                        <div
                            key={event.id}
                            className={styles.result}
                            onClick={()=>navigate(`/event/${event.id}`)}
                        >
                            {event.icon} {event.title}
                        </div>
                    ))

                )}

            </div>

        </div>

    );

}

export default SearchBar;