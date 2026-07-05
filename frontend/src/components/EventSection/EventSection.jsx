import events from "../../data/events";

import EventCard from "../EventCard/EventCard";

import styles from "./EventSection.module.css";

function EventSection() {

    return (

        <section className={styles.section}>

            <h2>

                📅 Today's AI Events

            </h2>

            <div className={styles.grid}>

                {events.map(event => (

                    <EventCard
                        key={event.id}
                        event={event}
                    />

                ))}

            </div>

        </section>

    );

}

export default EventSection;