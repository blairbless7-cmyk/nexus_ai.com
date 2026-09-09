import { useState, useEffect } from 'react';
import JobPostForm from '../../components/JobPostForm';
import ContractView from '../../components/ContractView';

export default function ClientDashboard() {
  const [token, setToken] = useState('');
    const [jobs, setJobs] = useState<any[]>([]);
      const [activeContractId, setActiveContractId] = useState<string>('');

        useEffect(() => {
            const t = localStorage.getItem('nexus_token') || '';
                setToken(t);
                    fetchJobs();
                      }, []);

                        const fetchJobs = async () => {
                            const res = await fetch('http://localhost:8000/api/v1/jobs/search?limit=20');
                                const data = await res.json();
                                    setJobs(data.results || []);
                                      };

                                        if (!token) return <div className="p-10 text-white">Please login first - token missing</div>;

                                          return (
                                              <div className="min-h-screen bg-black text-white p-6 space-y-8">
                                                    <h1 className="text-3xl font-black">Enterprise Client Dashboard</h1>
                                                          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                                                  <div className="space-y-6">
                                                                            <JobPostForm token={token} onPosted={fetchJobs} />
                                                                                      <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-xl">
                                                                                                  <h3 className="font-bold mb-3">Your Open Jobs</h3>
                                                                                                              {jobs.map((j: any) => (
                                                                                                                            <div key={j.id} className="border-b border-zinc-800 py-3 flex justify-between">
                                                                                                                                            <div><p className="font-bold">{j.title}</p><p className="text-xs text-zinc-500">${j.budget} - {j.skills?.join(', ')}</p></div>
                                                                                                                                                            <button onClick={() => alert(`To create contract: POST /contracts/create with job_id ${j.id} + talent_id from search`)} className="text-purple-400 text-sm">Hire</button>
                                                                                                                                                                          </div>
                                                                                                                                                                                      ))}
                                                                                                                                                                                                </div>
                                                                                                                                                                                                        </div>
                                                                                                                                                                                                                <div>
                                                                                                                                                                                                                          {activeContractId ? (
                                                                                                                                                                                                                                      <ContractView contractId={activeContractId} token={token} isClient={true} />
                                                                                                                                                                                                                                                ) : (
                                                                                                                                                                                                                                                            <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-xl">
                                                                                                                                                                                                                                                                          <p className="text-zinc-400">Create a contract first, then paste its ID here:</p>
                                                                                                                                                                                                                                                                                        <input placeholder="contract_id" className="w-full bg-black border border-zinc-700 p-2 rounded mt-3" onKeyDown={e => { if (e.key === 'Enter') setActiveContractId((e.target as any).value); }} />
                                                                                                                                                                                                                                                                                                    </div>
                                                                                                                                                                                                                                                                                                              )}
                                                                                                                                                                                                                                                                                                                      </div>
                                                                                                                                                                                                                                                                                                                            </div>
                                                                                                                                                                                                                                                                                                                                </div>
                                                                                                                                                                                                                                                                                                                                  );
                                                                                                                                                                                                                                                                                                                                  }