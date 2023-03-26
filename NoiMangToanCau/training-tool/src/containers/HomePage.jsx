import { Link } from "react-router-dom"
import "./HomePage.css"

export default function HomePage({listGame}) {
    return (
        <div className="home-page">
            <h1>Select a Game</h1>

            <div className="menu">
                {
                    listGame.map((game) => (
                        <div className="item" key={game.name}>
                            <Link to={game.link}>{game.name}</Link>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}