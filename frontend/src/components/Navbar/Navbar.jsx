import { Link, NavLink } from "react-router-dom";
import styles from "./Navbar.module.css";

function Navbar() {
  return (
    <header className={styles.header}>
      <div className={styles.container}>

        {/* Logo */}
        <Link to="/" className={styles.logo}>
          📰 NewsLens AI
        </Link>

        {/* Navigation */}
        <nav className={styles.navLinks}>
          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive ? styles.active : ""
            }
          >
            Home
          </NavLink>

          <NavLink
            to="/about"
            className={({ isActive }) =>
              isActive ? styles.active : ""
            }
          >
            About
          </NavLink>

          <button className={styles.searchButton}>
            🔍 Search
          </button>
        </nav>

      </div>
    </header>
  );
}

export default Navbar;