import { useNavigate } from "react-router-dom";

import styles from "./EventCard.module.css";

function EventCard({ event }) {

    const navigate = useNavigate();

    return (

        <div
            className={styles.card}
            onClick={() => navigate(`/event/${event.id}`)}
        >

            <h2>

                {event.icon} {event.title}

            </h2>

            <p>

                📰 {event.articles} Articles

            </p>

            <p>

                📡 {event.sources.join(" • ")}

            </p>

            <div className={styles.bottom}>

                <span>

                    🧠 Confidence {event.confidence}%

                </span>

                <button>

                    Read Summary →

                </button>

            </div>

        </div>

    );

}

export default EventCard;