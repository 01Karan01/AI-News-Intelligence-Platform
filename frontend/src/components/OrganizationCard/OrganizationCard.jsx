import { FiBriefcase } from "react-icons/fi";

import styles from "./OrganizationCard.module.css";

function OrganizationCard({ organizations }) {
  return (
    <section className={styles.card} aria-labelledby="organizations-title">
      <h2 id="organizations-title">Organizations</h2>
      <div className={styles.chips}>
        {organizations.map((organization) => (
          <span className={styles.chip} key={organization}>
            <FiBriefcase /> {organization}
          </span>
        ))}
      </div>
    </section>
  );
}

export default OrganizationCard;
