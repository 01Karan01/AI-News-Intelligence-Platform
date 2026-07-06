import EventCard from "../EventCard/EventCard";
import styles from "./DateSection.module.css";

function DateSection({ date, events }) {

    return (

        <section className={styles.section}>

            <h2>

                📅 {date}

            </h2>

            <div className={styles.grid}>

                {events.map(event=>(

                    <EventCard
                        key={event.id}
                        event={event}
                    />

                ))}

            </div>

        </section>

    );

}

export default DateSection;