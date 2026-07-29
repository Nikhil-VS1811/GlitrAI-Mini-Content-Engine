import JobCard from "./JobCard";

function JobList({ jobs }) {
  if (jobs.length === 0) {
    return <p>No jobs submitted yet.</p>;
  }

  return (
    <section>
      <h2>Jobs</h2>
      {jobs.map((job) => <JobCard key={job.id} job={job} />)}
    </section>
  );
}

export default JobList;
