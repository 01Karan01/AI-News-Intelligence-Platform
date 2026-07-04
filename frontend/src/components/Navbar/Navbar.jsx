import { Link } from "react-router-dom";

import styles from "./Navbar.module.css";

function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        📰 NewsLens AI
      </div>

      <div className={styles.links}>
        <Link to="/">Home</Link>

        <Link to="/about">About</Link>
      </div>
    </nav>
  );
}

export default Navbar;