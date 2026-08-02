import { FiUser } from "react-icons/fi";

import styles from "./PeopleCard.module.css";

function PeopleCard({ people = [] }) {
  const items = Array.isArray(people) ? people : [];
  if (items.length === 0) return null;

  return (
    <section className={styles.card} aria-labelledby="people-title">
      <h2 id="people-title">Key People</h2>
      <div className={styles.chips}>
        {items.map((person) => (
          <span className={styles.chip} key={person}>
            <FiUser /> {person}
          </span>
        ))}
      </div>
    </section>
  );
}

export default PeopleCard;

