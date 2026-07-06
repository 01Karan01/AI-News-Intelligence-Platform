import { motion } from "framer-motion";
import { FiArrowLeft, FiSearch } from "react-icons/fi";
import { Link } from "react-router-dom";

import styles from "./NotFound.module.css";

function NotFound() {
  return (
    <motion.section
      className={styles.page}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.24 }}
    >
      <div className={styles.illustration} aria-hidden="true">
        <FiSearch />
        <span />
        <span />
      </div>
      <p>404</p>
      <h1>Signal not found</h1>
      <span className={styles.copy}>
        This route is outside the current NewsLens AI intelligence index.
      </span>
      <Link to="/">
        <FiArrowLeft /> Back Home
      </Link>
    </motion.section>
  );
}

export default NotFound;
