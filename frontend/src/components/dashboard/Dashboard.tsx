'use client'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  ExclamationTriangleIcon, 
  CheckCircleIcon,
  ClockIcon 
} from '@heroicons/react/24/outline'

interface AttendanceData {
  currentPercentage: number
  safetyBuffer: number
  riskLevel: 'low' | 'medium' | 'high' | 'critical'
  recommendations: Recommendation[]
}

interface Recommendation {
  type: string
  message: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  suggested_actions?: string[]
}

export default function Dashboard() {
  const [attendanceData, setAttendanceData] = useState<AttendanceData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate loading attendance data
    setTimeout(() => {
      setAttendanceData({
        currentPercentage: 78.5,
        safetyBuffer: 8.0,
        riskLevel: 'low',
        recommendations: [
          {
            type: 'optimization',
            priority: 'low',
            message: 'You have excellent attendance! You can strategically skip classes you dislike.',
            suggested_actions: [
              'Skip up to 2 classes of disliked subjects this week',
              'Prioritize attending practical sessions',
              'Use free time for extracurricular activities'
            ]
          }
        ]
      })
      setLoading(false)
    }, 2000)
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!attendanceData) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No attendance data available</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        {/* Attendance Overview */}
        <div className="grid md:grid-cols-3 gap-6">
          <AttendanceCard
            title="Current Attendance"
            value={`${attendanceData.currentPercentage}%`}
            icon={ChartBarIcon}
            color={getRiskColor(attendanceData.riskLevel)}
          />
          <AttendanceCard
            title="Safety Buffer"
            value={`+${attendanceData.safetyBuffer}%`}
            icon={CheckCircleIcon}
            color="green"
          />
          <AttendanceCard
            title="Risk Level"
            value={attendanceData.riskLevel.toUpperCase()}
            icon={ExclamationTriangleIcon}
            color={getRiskColor(attendanceData.riskLevel)}
          />
        </div>

        {/* Progress Bar */}
        <motion.div
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Attendance Progress</h3>
          <div className="relative">
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div 
                className={`h-4 rounded-full transition-all duration-1000 ${
                  attendanceData.currentPercentage > 75 ? 'bg-green-500' :
                  attendanceData.currentPercentage > 70.5 ? 'bg-yellow-500' : 'bg-red-500'
                }`}
                style={{ width: `${Math.min(attendanceData.currentPercentage, 100)}%` }}
              ></div>
            </div>
            <div className="flex justify-between text-sm text-gray-600 mt-2">
              <span>0%</span>
              <span className="font-semibold">70.5% (Target)</span>
              <span>75% (Safe Zone)</span>
              <span>100%</span>
            </div>
          </div>
        </motion.div>

        {/* Recommendations */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Recommendations</h3>
          <div className="space-y-4">
            {attendanceData.recommendations.map((rec, index) => (
              <RecommendationCard key={index} recommendation={rec} />
            ))}
          </div>
        </motion.div>
      </motion.div>
    </div>
  )
}

function AttendanceCard({ 
  title, 
  value, 
  icon: Icon, 
  color 
}: { 
  title: string
  value: string
  icon: any
  color: string 
}) {
  const colorClasses = {
    green: 'bg-green-100 text-green-600',
    yellow: 'bg-yellow-100 text-yellow-600',
    red: 'bg-red-100 text-red-600',
    blue: 'bg-blue-100 text-blue-600'
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color as keyof typeof colorClasses]}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </motion.div>
  )
}

function RecommendationCard({ recommendation }: { recommendation: Recommendation }) {
  const priorityColors = {
    low: 'border-green-200 bg-green-50',
    medium: 'border-yellow-200 bg-yellow-50',
    high: 'border-orange-200 bg-orange-50',
    critical: 'border-red-200 bg-red-50'
  }

  return (
    <div className={`p-4 rounded-lg border-l-4 ${priorityColors[recommendation.priority]}`}>
      <div className="flex items-start space-x-3">
        <div className="flex-1">
          <p className="font-medium text-gray-900">{recommendation.message}</p>
          {recommendation.suggested_actions && (
            <ul className="mt-2 text-sm text-gray-600 space-y-1">
              {recommendation.suggested_actions.map((action, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span>•</span>
                  <span>{action}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
        <span className={`text-xs px-2 py-1 rounded-full font-medium ${
          recommendation.priority === 'critical' ? 'bg-red-100 text-red-800' :
          recommendation.priority === 'high' ? 'bg-orange-100 text-orange-800' :
          recommendation.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
          'bg-green-100 text-green-800'
        }`}>
          {recommendation.priority.toUpperCase()}
        </span>
      </div>
    </div>
  )
}

function getRiskColor(riskLevel: string): string {
  switch (riskLevel) {
    case 'low': return 'green'
    case 'medium': return 'yellow'
    case 'high': case 'critical': return 'red'
    default: return 'blue'
  }
}