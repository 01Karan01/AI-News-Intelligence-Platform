import { useMemo } from "react";

import { useEvents } from "../../hooks/useEvents";
import EventCard from "../EventCard/EventCard";
import styles from "./EventSection.module.css";

function EventSection() {
  const { events } = useEvents();
  const groupedEvents = useMemo(
    () =>
      events.reduce((groups, event) => {
        const key = new Date(event.date).toDateString();
        return { ...groups, [key]: [...(groups[key] ?? []), event] };
      }, {}),
    [events],
  );

  return (
    <section className={styles.section}>
      {Object.entries(groupedEvents).map(([date, grouped]) => (
        <div key={date} className={styles.daySection}>
          <h2>{date}</h2>
          <div className={styles.grid}>
            {grouped.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}

export default EventSection;
