// File: if/web/src/components/WelcomeHeader.tsx 
import { motion } from 
"framer-motion";

export default function WelcomeHeader() {
  return (
    <motion.div
      className="mb-6"
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      exit={{ opacity: 0, y: -10 }} >
      <h1 className="text-3xl font-bold tracking-tight">
        Welcome back to RTCA ✨
      </h1>
      <p className="text-zinc-500 dark:text-zinc-400 mt-1">
        Your AI assistant control room is up and running.
      </p>
    </motion.div>
  );
}

