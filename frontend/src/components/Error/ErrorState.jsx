import { FiAlertCircle, FiHome } from "react-icons/fi";
import { Link } from "react-router-dom";

import styles from "./ErrorState.module.css";

function ErrorState({ title = "Something went wrong", message, action = "Back Home" }) {
  return (
    <section className={styles.state} role="alert">
      <div className={styles.icon}>
        <FiAlertCircle />
      </div>
      <h1>{title}</h1>
      {message && <p>{message}</p>}
      <Link to="/">
        <FiHome /> {action}
      </Link>
    </section>
  );
}

export default ErrorState;
