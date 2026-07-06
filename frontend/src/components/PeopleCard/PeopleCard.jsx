import { FiUser } from "react-icons/fi";

import styles from "./PeopleCard.module.css";

function PeopleCard({ people }) {
  return (
    <section className={styles.card} aria-labelledby="people-title">
      <h2 id="people-title">Key People</h2>
      <div className={styles.chips}>
        {people.map((person) => (
          <span className={styles.chip} key={person}>
            <FiUser /> {person}
          </span>
        ))}
      </div>
    </section>
  );
}

export default PeopleCard;
