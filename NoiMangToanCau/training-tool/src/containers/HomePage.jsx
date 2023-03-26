import { Link } from "react-router-dom"
import "./HomePage.css"

export default function HomePage({listGame}) {
    return (
        <div className="home-page">
            <h1>Select a Game</h1>

            <div className="menu">
                {
                    listGame.map((game) => (
                        <Link to={game.link}>
                            <button className="item">
                                {game.name}
                            </button>
                        </Link>
                    ))
                }
            </div>
        </div>
    )
}