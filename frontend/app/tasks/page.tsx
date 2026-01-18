'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const TasksPage = () => {
  const router = useRouter();

  useEffect(() => {
    // Redirect to homepage since task functionality is now on the homepage
    router.push('/');
  }, [router]);

  return null;
};

export default TasksPage;