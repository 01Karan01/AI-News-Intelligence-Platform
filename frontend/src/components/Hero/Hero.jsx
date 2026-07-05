import styles from "./Hero.module.css";
import SearchBar from "../SearchBar/SearchBar";

function Hero() {

    return (

        <section className={styles.hero}>

            <div className={styles.content}>

                <p className={styles.badge}>
                    🚀 AI Powered News Intelligence
                </p>

                <h1>
                    Understand Events,
                    <br />
                    Not Headlines.
                </h1>

                <p className={styles.description}>
                    AI groups hundreds of news articles
                    into meaningful events so you can
                    understand what's happening in seconds.
                </p>

                <SearchBar />

            </div>

        </section>

    );

}

export default Hero;