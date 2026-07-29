import { useState } from "react";

function UploadForm({ onCreate }) {
  const [productName, setProductName] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (!image) {
      setError("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("product_name", productName);
    formData.append("description", description);
    formData.append("image", image);

    try {
      setIsSubmitting(true);
      await onCreate(formData);
      setProductName("");
      setDescription("");
      setImage(null);
      event.target.reset();
    } catch (requestError) {
      setError(requestError.response?.data?.detail ?? "Unable to create the job.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <label>
        Product Name
        <input
          type="text"
          value={productName}
          onChange={(event) => setProductName(event.target.value)}
          required
        />
      </label>

      <label>
        Description
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          required
          rows="4"
        />
      </label>

      <label>
        Image
        <input
          type="file"
          accept="image/jpeg,image/png,image/gif,image/webp"
          onChange={(event) => setImage(event.target.files?.[0] ?? null)}
          required
        />
      </label>

      {error && <p className="error-message">{error}</p>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Submitting..." : "Create Job"}
      </button>
    </form>
  );
}

export default UploadForm;
