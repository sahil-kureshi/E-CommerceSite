import React, { useEffect, useState } from "react";
import { getMyProfile, updateProfile } from "../api/authApi";

function Profile() {
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({});
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getMyProfile();
        setProfile(data);
        setFormData(data);
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };
    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const updated = await updateProfile(formData);
      setProfile(updated);
      setEditing(false);
      alert("Profile updated successfully!");
    } catch (error) {
      alert("Update failed: " + error.response?.data?.detail);
    }
  };

  if (!profile) return <p>Loading profile...</p>;

  return (
    <div className="profile-page">
      <h2>My Profile</h2>
      {editing ? (
        <form onSubmit={handleUpdate}>
          <input name="name" value={formData.name} onChange={handleChange} required />
          <input name="email" value={formData.email} onChange={handleChange} required />
          <input name="phone" value={formData.phone || ""} onChange={handleChange} />
          <input name="address" value={formData.address || ""} onChange={handleChange} />
          <button type="submit">Save</button>
          <button type="button" onClick={() => setEditing(false)}>Cancel</button>
        </form>
      ) : (
        <div className="profile-info">
          <p><strong>Name:</strong> {profile.name}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Phone:</strong> {profile.phone || "Not provided"}</p>
          <p><strong>Address:</strong> {profile.address || "Not provided"}</p>
          <button onClick={() => setEditing(true)}>Edit Profile</button>
        </div>
      )}
    </div>
  );
}

export default Profile;