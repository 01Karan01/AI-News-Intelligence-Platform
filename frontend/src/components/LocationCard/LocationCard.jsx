import { FiMapPin } from "react-icons/fi";

import styles from "./LocationCard.module.css";

function LocationCard({ locations = [] }) {
  const items = Array.isArray(locations) ? locations : [];
  if (items.length === 0) return null;

  return (
    <section className={styles.card} aria-labelledby="locations-title">
      <h2 id="locations-title">Locations</h2>
      <div className={styles.chips}>
        {items.map((location) => (
          <span className={styles.chip} key={location}>
            <FiMapPin /> {location}
          </span>
        ))}
      </div>
    </section>
  );
}

export default LocationCard;

