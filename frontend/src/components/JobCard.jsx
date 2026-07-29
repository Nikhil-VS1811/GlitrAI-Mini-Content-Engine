import { getGeneratedImageUrl } from "../services/api";

function JobCard({ job }) {
  const imageUrl = getGeneratedImageUrl(job.generated_image);

  return (
    <article className="job-card">
      <p><strong>Job ID:</strong> {job.id}</p>
      <p><strong>Status:</strong> {job.status}</p>
      <p><strong>Generated Prompt:</strong> {job.generated_prompt ?? "Waiting for generation..."}</p>
      {imageUrl && (
        <div>
          <strong>Generated Image:</strong>
          <img src={imageUrl} alt="Generated product result" className="generated-image" />
        </div>
      )}
    </article>
  );
}

export default JobCard;
