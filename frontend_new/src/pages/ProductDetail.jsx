import React, { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { getProductById } from "../api/productsApi";
import { CartContext } from "../context/CartContext";

function ProductDetail() {
  const { id } = useParams(); // product ID from URL
  const [product, setProduct] = useState(null);
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await getProductById(id);
        setProduct(data);
      } catch (error) {
        console.error("Error fetching product:", error);
      }
    };
    fetchProduct();
  }, [id]);

  if (!product) return <p>Loading product details...</p>;

  return (
    <div className="product-detail">
      <img src={product.image_url} alt={product.name} width="250" />
      <h2>{product.name}</h2>
      <p><strong>Category:</strong> {product.category}</p>
      <p><strong>Price:</strong> ₹{product.price}</p>
      <p><strong>Stock:</strong> {product.stock > 0 ? "Available" : "Out of Stock"}</p>
      <p>{product.description}</p>
      {product.stock > 0 && (
        <button onClick={() => addToCart(product, 1)}>Add to Cart</button>
      )}
    </div>
  );
}

export default ProductDetail;