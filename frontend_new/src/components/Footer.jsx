import React from "react";
import { Link } from "react-router-dom";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <h3>Sahil Footwear</h3>
        <p>Stylish, comfortable, and affordable footwear for everyone.</p>

        <ul className="footer-links">
          <li><Link to="/about">About Us</Link></li>
          <li><Link to="/contact">Contact</Link></li>
          <li><Link to="/privacy">Privacy Policy</Link></li>
        </ul>

        <p className="footer-copy">
          © {new Date().getFullYear()} Sahil Footwear. All rights reserved.
        </p>
      </div>
    </footer>
  );
}

export default Footer;