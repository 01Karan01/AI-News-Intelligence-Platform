import styles from "./PageLoader.module.css";

function PageLoader({ label = "Loading intelligence" }) {
  return (
    <div className={styles.loader} role="status" aria-live="polite">
      <span />
      <p>{label}</p>
    </div>
  );
}

export default PageLoader;
