import EventCard from "../EventCard/EventCard";
import styles from "./TrendingEvents.module.css";

function TrendingEvents({ events }) {
  return (
    <section className={styles.section} aria-labelledby="trending-events-title">
      <div className={styles.header}>
        <span>High velocity clusters</span>
        <h2 id="trending-events-title">Today's Events</h2>
      </div>
      <div className={styles.grid}>
        {events.map((event) => (
          <EventCard event={event} key={event.id} />
        ))}
      </div>
    </section>
  );
}

export default TrendingEvents;
