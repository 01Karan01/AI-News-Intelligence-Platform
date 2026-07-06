import { motion } from "framer-motion";
import { FiActivity, FiGlobe, FiZap } from "react-icons/fi";

import SearchBar from "../SearchBar/SearchBar";
import styles from "./Hero.module.css";

function Hero() {
  return (
    <section className={styles.hero} aria-labelledby="hero-title">
      <motion.div
        className={styles.content}
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <div className={styles.badge}>
          <FiZap />
          <span>AI clustered news intelligence</span>
        </div>
        <h1 id="hero-title">NewsLens AI</h1>
        <p>
          Track breaking stories across sources, understand how articles connect, and inspect
          the people, organizations, and locations shaping each event.
        </p>
        <SearchBar variant="hero" />
        <div className={styles.metrics} aria-label="Platform capabilities">
          <span>
            <FiActivity /> Live event clustering
          </span>
          <span>
            <FiGlobe /> Global source coverage
          </span>
        </div>
      </motion.div>
      <motion.div
        className={styles.visual}
        aria-hidden="true"
        initial={{ opacity: 0, scale: 0.96 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.14, duration: 0.5 }}
      >
        <div className={styles.mapPanel}>
          <span className={styles.pulseOne} />
          <span className={styles.pulseTwo} />
          <span className={styles.pulseThree} />
          <div className={styles.signalCard}>
            <strong>94%</strong>
            <span>AI confidence</span>
          </div>
        </div>
      </motion.div>
    </section>
  );
}

export default Hero;
