import React, { useEffect, useState, useContext } from "react";
import { getProducts } from "../api/productsApi";
import { CartContext } from "../context/CartContext";

function Products() {
  const [products, setProducts] = useState([]);
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await getProducts();
        setProducts(data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchProducts();
  }, []);

  if (products.length === 0) return <p>Loading products...</p>;

  return (
    <div className="products-page">
      <h2>Our Products</h2>
      <div className="product-grid">
        {products.map((product) => (
          <div key={product.product_id} className="product-card">
            <img src={product.image_url} alt={product.name} width="150" />
            <h3>{product.name}</h3>
            <p>{product.category}</p>
            <p>₹{product.price}</p>
            <button onClick={() => addToCart(product, 1)}>Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Products;