import { FiMapPin } from "react-icons/fi";

import styles from "./LocationCard.module.css";

function LocationCard({ locations }) {
  return (
    <section className={styles.card} aria-labelledby="locations-title">
      <h2 id="locations-title">Locations</h2>
      <div className={styles.chips}>
        {locations.map((location) => (
          <span className={styles.chip} key={location}>
            <FiMapPin /> {location}
          </span>
        ))}
      </div>
    </section>
  );
}

export default LocationCard;
