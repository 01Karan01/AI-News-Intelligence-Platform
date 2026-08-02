import { memo } from "react";
import { motion } from "framer-motion";
import { FiArrowRight, FiFileText, FiUsers, FiZap } from "react-icons/fi";
import { Link } from "react-router-dom";

import { cleanDisplayText } from "../../utils/text";
import styles from "./EventCard.module.css";

function EventCard({ event, compact = false }) {
  const date = new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(event.date));

  return (
    <motion.article
      className={`${styles.card} ${compact ? styles.compact : ""}`}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.18 }}
    >
      <div className={styles.topline}>
        <span className={styles.icon} aria-hidden="true">
          <FiZap />
        </span>
        <span>{event.category}</span>
        <time dateTime={event.date}>{date}</time>
      </div>
      <h3>{cleanDisplayText(event.title, "Untitled event")}</h3>
      <p>{cleanDisplayText(event.summary, "No summary is available for this event cluster.")}</p>
      <div className={styles.meta} aria-label="Event metrics">
        <span>
          <FiFileText /> {event.articleCount} articles
        </span>
        <span>
          <FiZap /> {event.confidence}% confidence
        </span>
        <span>
          <FiUsers /> {event.people.length} people
        </span>
      </div>
      <Link className={styles.button} to={`/event/${event.id}`}>
        View Summary
        <FiArrowRight />
      </Link>
    </motion.article>
  );
}

export default memo(EventCard);
