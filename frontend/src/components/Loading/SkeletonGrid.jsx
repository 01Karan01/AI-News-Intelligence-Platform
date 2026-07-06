import styles from "./SkeletonGrid.module.css";

function SkeletonGrid({ count = 4 }) {
  return (
    <div className={styles.grid} aria-label="Loading content">
      {Array.from({ length: count }, (_, index) => (
        <div className={styles.card} key={index}>
          <span />
          <strong />
          <p />
          <p />
          <em />
        </div>
      ))}
    </div>
  );
}

export default SkeletonGrid;
