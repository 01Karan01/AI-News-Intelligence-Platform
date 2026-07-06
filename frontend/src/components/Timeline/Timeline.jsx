import EventCard from "../EventCard/EventCard";
import styles from "./Timeline.module.css";

function Timeline({ groups }) {
  return (
    <section className={styles.section} aria-labelledby="timeline-title">
      <div className={styles.header}>
        <span>Previous 5 days</span>
        <h2 id="timeline-title">Event Timeline</h2>
      </div>
      <div className={styles.timeline}>
        {groups.map((group) => (
          <article className={styles.group} key={group.label}>
            <div className={styles.rail}>
              <span />
            </div>
            <div className={styles.content}>
              <h3>{group.label}</h3>
              {group.events.length > 0 ? (
                <div className={styles.cards}>
                  {group.events.map((event) => (
                    <EventCard compact event={event} key={event.id} />
                  ))}
                </div>
              ) : (
                <p className={styles.empty}>No major AI-clustered events detected.</p>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default Timeline;
