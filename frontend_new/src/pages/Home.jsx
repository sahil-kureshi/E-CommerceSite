import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-page">
      <h1>Welcome to Sahil Footwear</h1>
      <p>Discover stylish and comfortable footwear at the best prices.</p>
      <Link to="/products">
        <button>Shop Now</button>
      </Link>
    </div>
  );
}

export default Home;