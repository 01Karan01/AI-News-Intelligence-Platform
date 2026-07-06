import { FiExternalLink } from "react-icons/fi";

import styles from "./RelatedArticles.module.css";

function RelatedArticles({ articles }) {
  return (
    <section className={styles.card} aria-labelledby="related-title">
      <div className={styles.header}>
        <h2 id="related-title">Related Articles</h2>
        <span>{articles.length} sources</span>
      </div>
      <div className={styles.list}>
        {articles.map((article) => (
          <article className={styles.article} key={article.id}>
            <div>
              <h3>{article.headline}</h3>
              <p>
                {article.source} •{" "}
                <time dateTime={article.publishedAt}>
                  {new Intl.DateTimeFormat("en", {
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  }).format(new Date(article.publishedAt))}
                </time>
              </p>
            </div>
            <a href={article.url} target="_blank" rel="noreferrer">
              Read Original
              <FiExternalLink />
            </a>
          </article>
        ))}
      </div>
    </section>
  );
}

export default RelatedArticles;
