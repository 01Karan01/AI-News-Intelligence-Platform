import { FiGithub, FiSearch } from "react-icons/fi";
import { Link } from "react-router-dom";

import styles from "./Footer.module.css";

function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <Link className={styles.brand} to="/">
          <FiSearch /> NewsLens AI
        </Link>
        <p>AI-powered news intelligence for event clustering, summaries, and entity discovery.</p>
        <a href="https://github.com" target="_blank" rel="noreferrer" aria-label="Open GitHub repository">
          <FiGithub /> GitHub
        </a>
      </div>
    </footer>
  );
}

export default Footer;
