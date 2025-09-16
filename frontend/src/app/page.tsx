'use client'
import { motion } from 'framer-motion'
import { 
  DocumentArrowUpIcon, 
  CpuChipIcon, 
  ChartBarIcon,
  ShieldCheckIcon 
} from '@heroicons/react/24/outline'
import Navbar from '@/components/layout/Navbar'

export default function LandingPage() {
  return (
    <>
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <motion.section 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Smart Attendance Planning with 
            <span className="text-blue-600"> AI</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload your college calendar and timetable, let AI analyze your preferences, 
            and get intelligent recommendations to maintain 70.5% attendance safely.
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Get Started
          </motion.button>
        </motion.section>

        {/* Features Section */}
        <motion.section 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.8 }}
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-8"
        >
          <FeatureCard
            icon={DocumentArrowUpIcon}
            title="PDF Processing"
            description="Upload calendar PDFs and timetable images for automatic parsing"
          />
          <FeatureCard
            icon={CpuChipIcon}
            title="AI Preferences"
            description="AI learns your subject preferences and recommends optimal attendance"
          />
          <FeatureCard
            icon={ChartBarIcon}
            title="Trip Planning"
            description="Plan holidays and see exact impact on your attendance percentage"
          />
          <FeatureCard
            icon={ShieldCheckIcon}
            title="Safety Buffer"
            description="Maintain 70.5% target with built-in safety margin for emergencies"
          />
        </motion.section>
      </main>
    </>
  )
}

function FeatureCard({ icon: Icon, title, description }: {
  icon: any,
  title: string,
  description: string
}) {
  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="bg-white p-6 rounded-xl shadow-lg border border-gray-100"
    >
      <div className="bg-blue-100 p-3 rounded-lg inline-block mb-4">
        <Icon className="h-6 w-6 text-blue-600" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </motion.div>
  )
}
