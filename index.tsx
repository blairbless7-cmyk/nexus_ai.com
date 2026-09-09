import { useEffect } from 'react';
import { useRouter } from 'next/router';
export default function Home() {
  const router = useRouter();
    useEffect(() => { router.push('/login'); }, []);
      return <div className="bg-black text-white p-10">Redirecting to /login...</div>;
      }