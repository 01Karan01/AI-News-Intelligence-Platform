import { FiActivity, FiArrowLeft, FiGlobe, FiLink } from "react-icons/fi";
import { Link } from "react-router-dom";

import LocationCard from "../LocationCard/LocationCard";
import OrganizationCard from "../OrganizationCard/OrganizationCard";
import PeopleCard from "../PeopleCard/PeopleCard";
import RelatedArticles from "../RelatedArticles/RelatedArticles";
import { cleanDisplayText } from "../../utils/text";
import styles from "./EventDetails.module.css";

function EventDetails({ event }) {
  const date = new Intl.DateTimeFormat("en", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(new Date(event.date));

  return (
    <article className={styles.page}>
      <Link className={styles.back} to="/">
        <FiArrowLeft /> Back to dashboard
      </Link>
      <header className={styles.hero}>
        <div>
          <span className={styles.category}>{event.category}</span>
          <h1>{cleanDisplayText(event.title, "Untitled event")}</h1>
          <time dateTime={event.date}>{date}</time>
        </div>
        <div className={styles.confidence} aria-label={`AI confidence score ${event.confidence}%`}>
          <strong>{event.confidence}%</strong>
          <span>AI Confidence</span>
          <progress className={styles.progress} value={event.confidence} max="100">
            {event.confidence}%
          </progress>
        </div>
      </header>

      <section className={styles.insights}>
        <div className={styles.summaryCard}>
          <FiActivity />
          <h2>AI Summary</h2>
          <p>{cleanDisplayText(event.summary, "No summary is available for this event cluster.")}</p>
        </div>
        <div className={styles.impactCard}>
          <FiGlobe />
          <h2>Global Impact</h2>
          <p>{event.globalImpact}</p>
        </div>
      </section>

      <section className={styles.eventTimeline} aria-labelledby="event-timeline-title">
        <h2 id="event-timeline-title">Timeline</h2>
        <ol>
          {(event.timeline || []).map((item) => (
            <li key={`${item.time}-${item.label}`}>
              <time>{item.time}</time>
              <span>{cleanDisplayText(item.label, "Article published")}</span>
            </li>
          ))}
        </ol>
      </section>

      <div className={styles.entities}>
        <PeopleCard people={event.people} />
        <OrganizationCard organizations={event.organizations} />
        <LocationCard locations={event.locations} />
      </div>

      <RelatedArticles articles={event.sources} />

      {(event.sources || []).length > 0 && (
        <section className={styles.sources} aria-labelledby="sources-title">
          <h2 id="sources-title">Original Source Links</h2>
          <div>
            {(event.sources || []).map((source) => (
              <a href={source.url} key={source.id} target="_blank" rel="noreferrer">
                <FiLink />
                {source.source}
              </a>
            ))}
          </div>
        </section>
      )}
    </article>
  );
}

export default EventDetails;

