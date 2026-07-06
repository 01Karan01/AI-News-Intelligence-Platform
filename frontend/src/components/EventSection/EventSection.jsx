import events from "../../data/events";
import EventCard from "../EventCard/EventCard";
import styles from "./EventSection.module.css";

function EventSection() {

    const groupedEvents = events.reduce((acc, event) => {

        if (!acc[event.date]) {

            acc[event.date] = [];

        }

        acc[event.date].push(event);

        return acc;

    }, {});

    const dates = Object.keys(groupedEvents).sort().reverse();

    return (

        <section className={styles.section}>

            {dates.map(date => (

                <div key={date} className={styles.daySection}>

                    <h2>📅 {date}</h2>

                    <div className={styles.grid}>

                        {groupedEvents[date].map(event => (

                            <EventCard
                                key={event.id}
                                event={event}
                            />

                        ))}

                    </div>

                </div>

            ))}

        </section>

    );

}

export default EventSection;