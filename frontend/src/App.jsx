import { useEffect, useState } from "react";

import JobList from "./components/JobList";
import UploadForm from "./components/UploadForm";
import { createJob, getJob } from "./services/api";


const FINAL_STATUSES = new Set(["completed", "failed"]);


function App() {
  const [jobs, setJobs] = useState([]);

  async function handleCreateJob(formData) {
    const createdJob = await createJob(formData);
    setJobs((currentJobs) => [
      {
        id: createdJob.job_id,
        status: createdJob.status,
        generated_prompt: null,
        generated_image: null,
      },
      ...currentJobs,
    ]);
  }

  useEffect(() => {
    const unfinishedJobs = jobs.filter((job) => !FINAL_STATUSES.has(job.status));
    if (unfinishedJobs.length === 0) {
      return undefined;
    }

    const intervalId = window.setInterval(async () => {
      const updates = await Promise.all(
        unfinishedJobs.map(async (job) => {
          try {
            return await getJob(job.id);
          } catch (error) {
            console.error(`Unable to poll job ${job.id}`, error);
            return null;
          }
        }),
      );

      const jobsById = new Map(
        updates.filter(Boolean).map((job) => [job.id, job]),
      );
      if (jobsById.size > 0) {
        setJobs((currentJobs) => currentJobs.map(
          (job) => jobsById.get(job.id) ?? job,
        ));
      }
    }, 3000);

    return () => window.clearInterval(intervalId);
  }, [jobs]);

  return (
    <main>
      <h1>Mini Content Engine</h1>
      <UploadForm onCreate={handleCreateJob} />
      <JobList jobs={jobs} />
    </main>
  );
}

export default App;
