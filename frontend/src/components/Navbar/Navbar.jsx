import { useState } from "react";
import { FiGithub, FiMenu, FiSearch, FiX } from "react-icons/fi";
import { NavLink } from "react-router-dom";

import styles from "./Navbar.module.css";

const links = [
  { label: "Home", to: "/" },
  { label: "About", to: "/about" },
];

function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className={styles.header}>
      <nav className={styles.nav} aria-label="Primary navigation">
        <NavLink className={styles.logo} to="/" onClick={() => setOpen(false)}>
          <span className={styles.logoMark} aria-hidden="true">
            <FiSearch />
          </span>
          <span>NewsLens AI</span>
        </NavLink>

        <button
          className={styles.menuButton}
          type="button"
          aria-label={open ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={open}
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <FiX /> : <FiMenu />}
        </button>

        <div className={`${styles.links} ${open ? styles.open : ""}`}>
          {links.map((link) => (
            <NavLink
              className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ""}`}
              key={link.to}
              to={link.to}
              onClick={() => setOpen(false)}
            >
              {link.label}
            </NavLink>
          ))}
          <a
            className={styles.github}
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            aria-label="Open project GitHub repository"
          >
            <FiGithub />
            <span>GitHub</span>
          </a>
        </div>
      </nav>
    </header>
  );
}

export default Navbar;
