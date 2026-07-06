import { FiFileText, FiGlobe, FiLayers, FiRadio } from "react-icons/fi";

import styles from "./Statistics.module.css";

const cards = [
  { key: "articles", label: "Articles", icon: FiFileText },
  { key: "events", label: "Events", icon: FiLayers },
  { key: "sources", label: "Sources", icon: FiRadio },
  { key: "countries", label: "Countries", icon: FiGlobe },
];

function Statistics({ statistics }) {
  return (
    <section className={styles.grid} aria-label="Dashboard statistics">
      {cards.map(({ key, label, icon: Icon }) => (
        <article className={styles.card} key={key}>
          <span className={styles.icon}>
            <Icon aria-hidden="true" />
          </span>
          <div>
            <strong>{statistics?.[key]?.toLocaleString() ?? "0"}</strong>
            <span>{label}</span>
          </div>
        </article>
      ))}
    </section>
  );
}

export default Statistics;
